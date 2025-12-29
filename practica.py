import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
from typing import List, Dict, Optional, Callable
from abc import ABC, abstractmethod
import json
import csv
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
from collections import Counter

# Para generar PDFs
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ ReportLab no está instalado. Instale con: pip install reportlab")

# Para scanner de código de barras
try:
    import cv2
    from pyzbar import pyzbar
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False
    print("⚠️ Librerías de barcode no disponibles. Instale con: pip install opencv-python pyzbar")


# ============= ENUMERACIONES =============

class MovementType(Enum):
    """Tipos de movimiento de inventario"""
    ENTRY = "entry"
    EXIT = "exit"


class AlertLevel(Enum):
    """Niveles de alerta de stock"""
    CRITICAL = "critical"
    LOW = "low"
    NORMAL = "normal"


# ============= MODELOS DE DOMINIO =============

@dataclass
class Product:
    """Modelo de producto con validaciones"""
    code: str
    name: str
    description: str
    price: float
    min_stock: int
    category: str = "General"
    barcode: str = ""
    
    def __post_init__(self):
        if not self.code or not self.name:
            raise ValueError("Código y nombre son obligatorios")
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.min_stock < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class StockMovement:
    """Modelo de movimiento de stock"""
    product_code: str
    quantity: int
    movement_type: MovementType
    description: str
    user: str
    timestamp: datetime
    
    def __init__(self, product_code: str, quantity: int, movement_type: MovementType, 
                 description: str = "", user: str = "Sistema"):
        self.product_code = product_code
        self.quantity = quantity
        self.movement_type = movement_type
        self.description = description
        self.user = user
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'product_code': self.product_code,
            'quantity': self.quantity,
            'movement_type': self.movement_type.value,
            'description': self.description,
            'user': self.user,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


class InventoryItem:
    """Gestión de stock con análisis avanzado"""
    
    def __init__(self, product: Product, quantity: int = 0):
        self._product = product
        self._quantity = quantity
        self._reserved_quantity = 0
    
    @property
    def product(self) -> Product:
        return self._product
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @property
    def available_quantity(self) -> int:
        """Cantidad disponible (total - reservado)"""
        return self._quantity - self._reserved_quantity
    
    @property
    def reserved_quantity(self) -> int:
        return self._reserved_quantity
    
    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self._quantity += quantity
    
    def remove_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if quantity > self.available_quantity:
            raise ValueError(f"Stock insuficiente. Disponible: {self.available_quantity}")
        self._quantity -= quantity
    
    def reserve_stock(self, quantity: int) -> None:
        """Reservar stock para pedidos"""
        if quantity > self.available_quantity:
            raise ValueError(f"No hay suficiente stock disponible para reservar")
        self._reserved_quantity += quantity
    
    def get_alert_level(self) -> AlertLevel:
        """Determinar el nivel de alerta del stock"""
        if self._quantity < (self._product.min_stock * 0.25):
            return AlertLevel.CRITICAL
        elif self._quantity < self._product.min_stock:
            return AlertLevel.LOW
        return AlertLevel.NORMAL
    
    def get_stock_percentage(self) -> float:
        """Porcentaje del stock respecto al mínimo"""
        if self._product.min_stock == 0:
            return 100.0
        return (self._quantity / self._product.min_stock) * 100
    
    def to_dict(self) -> Dict:
        return {
            'product': self._product.to_dict(),
            'quantity': self._quantity,
            'available_quantity': self.available_quantity,
            'reserved_quantity': self._reserved_quantity,
            'alert_level': self.get_alert_level().value,
            'stock_percentage': self.get_stock_percentage()
        }


# ============= REPOSITORIOS =============

class Repository(ABC):
    """Interfaz base para repositorios con operaciones CRUD"""
    
    @abstractmethod
    def add(self, item) -> None:
        pass
    
    @abstractmethod
    def get(self, identifier) -> Optional[any]:
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def update(self, identifier, item) -> None:
        pass
    
    @abstractmethod
    def delete(self, identifier) -> None:
        pass
    
    @abstractmethod
    def exists(self, identifier) -> bool:
        pass


class ProductRepository(Repository):
    """Repositorio de productos con capacidades de búsqueda"""
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
    
    def add(self, product: Product) -> None:
        if self.exists(product.code):
            raise ValueError(f"El producto {product.code} ya existe")
        self._products[product.code] = product
    
    def get(self, code: str) -> Optional[Product]:
        return self._products.get(code)
    
    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        """Buscar producto por código de barras"""
        for product in self._products.values():
            if product.barcode == barcode:
                return product
        return None
    
    def get_all(self) -> List[Product]:
        return list(self._products.values())
    
    def update(self, code: str, product: Product) -> None:
        if not self.exists(code):
            raise ValueError(f"El producto {code} no existe")
        self._products[code] = product
    
    def delete(self, code: str) -> None:
        if code in self._products:
            del self._products[code]
    
    def exists(self, code: str) -> bool:
        return code in self._products
    
    def search(self, query: str) -> List[Product]:
        """Buscar productos por código o nombre"""
        query_lower = query.lower()
        return [p for p in self._products.values() 
                if query_lower in p.code.lower() or query_lower in p.name.lower()]
    
    def get_by_category(self, category: str) -> List[Product]:
        """Obtener productos por categoría"""
        return [p for p in self._products.values() if p.category == category]
    
    def get_categories(self) -> List[str]:
        """Obtener todas las categorías únicas"""
        return list(set(p.category for p in self._products.values()))


class MovementRepository(Repository):
    """Repositorio de movimientos con filtros avanzados"""
    
    def __init__(self):
        self._movements: List[StockMovement] = []
    
    def add(self, movement: StockMovement) -> None:
        self._movements.append(movement)
    
    def get(self, index: int) -> Optional[StockMovement]:
        if 0 <= index < len(self._movements):
            return self._movements[index]
        return None
    
    def get_all(self) -> List[StockMovement]:
        return self._movements.copy()
    
    def update(self, index: int, movement: StockMovement) -> None:
        if 0 <= index < len(self._movements):
            self._movements[index] = movement
    
    def delete(self, index: int) -> None:
        if 0 <= index < len(self._movements):
            del self._movements[index]
    
    def exists(self, index: int) -> bool:
        return 0 <= index < len(self._movements)
    
    def get_by_product(self, product_code: str) -> List[StockMovement]:
        """Obtener movimientos de un producto específico"""
        return [m for m in self._movements if m.product_code == product_code]
    
    def get_by_type(self, movement_type: MovementType) -> List[StockMovement]:
        """Obtener movimientos por tipo"""
        return [m for m in self._movements if m.movement_type == movement_type]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[StockMovement]:
        """Obtener movimientos en un rango de fechas"""
        return [m for m in self._movements 
                if start_date <= m.timestamp <= end_date]


# ============= SERVICIOS DE NEGOCIO =============

class InventoryService:
    """Servicio principal de gestión de inventario"""
    
    def __init__(self, product_repo: ProductRepository, movement_repo: MovementRepository):
        self._product_repo = product_repo
        self._movement_repo = movement_repo
        self._inventory: Dict[str, InventoryItem] = {}
        self._observers: List[Callable] = []
    
    def add_observer(self, observer: Callable) -> None:
        """Añadir observador para cambios en el inventario"""
        self._observers.append(observer)
    
    def _notify_observers(self) -> None:
        """Notificar a todos los observadores"""
        for observer in self._observers:
            observer()
    
    def register_product(self, product: Product, initial_quantity: int = 0, user: str = "Sistema") -> None:
        """Registrar un nuevo producto"""
        if self._product_repo.exists(product.code):
            raise ValueError(f"El producto {product.code} ya existe")
        
        self._product_repo.add(product)
        self._inventory[product.code] = InventoryItem(product, initial_quantity)
        
        if initial_quantity > 0:
            movement = StockMovement(
                product.code, initial_quantity, 
                MovementType.ENTRY, "Stock inicial", user
            )
            self._movement_repo.add(movement)
        
        self._notify_observers()
    
    def add_stock(self, product_code: str, quantity: int, description: str = "", user: str = "Sistema") -> None:
        """Agregar stock a un producto"""
        if product_code not in self._inventory:
            raise ValueError(f"Producto {product_code} no encontrado")
        
        self._inventory[product_code].add_stock(quantity)
        movement = StockMovement(product_code, quantity, MovementType.ENTRY, description, user)
        self._movement_repo.add(movement)
        self._notify_observers()
    
    def remove_stock(self, product_code: str, quantity: int, description: str = "", user: str = "Sistema") -> None:
        """Remover stock de un producto"""
        if product_code not in self._inventory:
            raise ValueError(f"Producto {product_code} no encontrado")
        
        self._inventory[product_code].remove_stock(quantity)
        movement = StockMovement(product_code, quantity, MovementType.EXIT, description, user)
        self._movement_repo.add(movement)
        self._notify_observers()
    
    def reserve_stock(self, product_code: str, quantity: int) -> None:
        """Reservar stock para pedidos"""
        if product_code not in self._inventory:
            raise ValueError(f"Producto {product_code} no encontrado")
        
        self._inventory[product_code].reserve_stock(quantity)
        self._notify_observers()
    
    def get_inventory_item(self, product_code: str) -> Optional[InventoryItem]:
        """Obtener item de inventario"""
        return self._inventory.get(product_code)
    
    def get_all_inventory_items(self) -> List[InventoryItem]:
        """Obtener todos los items del inventario"""
        return list(self._inventory.values())
    
    def get_low_stock_items(self) -> List[InventoryItem]:
        """Obtener productos con stock bajo"""
        return [item for item in self._inventory.values() 
                if item.get_alert_level() != AlertLevel.NORMAL]
    
    def get_critical_stock_items(self) -> List[InventoryItem]:
        """Obtener productos con stock crítico"""
        return [item for item in self._inventory.values() 
                if item.get_alert_level() == AlertLevel.CRITICAL]
    
    def get_total_inventory_value(self) -> float:
        """Calcular valor total del inventario"""
        return sum(item.quantity * item.product.price 
                   for item in self._inventory.values())
    
    def get_inventory_statistics(self) -> Dict:
        """Obtener estadísticas del inventario"""
        items = list(self._inventory.values())
        return {
            'total_products': len(items),
            'total_items': sum(item.quantity for item in items),
            'total_value': self.get_total_inventory_value(),
            'low_stock_count': len(self.get_low_stock_items()),
            'critical_stock_count': len(self.get_critical_stock_items()),
            'categories': len(self._product_repo.get_categories())
        }
    
    def get_most_sold_products(self, limit: int = 10) -> List[tuple]:
        """Obtener productos más vendidos"""
        exits = self._movement_repo.get_by_type(MovementType.EXIT)
        sales_counter = Counter()
        
        for movement in exits:
            sales_counter[movement.product_code] += movement.quantity
        
        return sales_counter.most_common(limit)
    
    def get_least_sold_products(self, limit: int = 10) -> List[tuple]:
        """Obtener productos menos vendidos"""
        exits = self._movement_repo.get_by_type(MovementType.EXIT)
        sales_counter = Counter()
        
        # Incluir todos los productos
        for item in self._inventory.values():
            sales_counter[item.product.code] = 0
        
        for movement in exits:
            sales_counter[movement.product_code] += movement.quantity
        
        # Ordenar de menor a mayor
        return sorted(sales_counter.items(), key=lambda x: x[1])[:limit]


# ============= GENERADORES DE REPORTES =============

class ReportGenerator(ABC):
    """Clase abstracta para generadores de reportes"""
    
    @abstractmethod
    def generate(self, service: InventoryService) -> str:
        pass
    
    @abstractmethod
    def export_csv(self, service: InventoryService, filename: str) -> None:
        pass
    
    def export_pdf(self, service: InventoryService, filename: str) -> None:
        """Método por defecto para PDF (puede ser sobrescrito)"""
        if not PDF_AVAILABLE:
            raise Exception("ReportLab no está instalado")


class InventoryReport(ReportGenerator):
    """Reporte completo de inventario"""
    
    def generate(self, service: InventoryService) -> str:
        items = service.get_all_inventory_items()
        stats = service.get_inventory_statistics()
        
        report = "=" * 100 + "\n"
        report += " " * 35 + "REPORTE DE INVENTARIO ACTUAL\n"
        report += "=" * 100 + "\n\n"
        
        report += f"Total de Productos: {stats['total_products']}\n"
        report += f"Total de Items: {stats['total_items']}\n"
        report += f"Valor Total: S/ {stats['total_value']:,.2f}\n"
        report += f"Productos con Stock Bajo: {stats['low_stock_count']}\n"
        report += f"Productos Críticos: {stats['critical_stock_count']}\n\n"
        
        report += "-" * 100 + "\n"
        report += f"{'Código':<10} {'Nombre':<25} {'Categoría':<15} {'Stock':<8} {'Reserv.':<8} {'Disp.':<8} {'Estado':<12}\n"
        report += "-" * 100 + "\n"
        
        for item in sorted(items, key=lambda x: x.product.code):
            alert = item.get_alert_level()
            status = "🔴 CRÍTICO" if alert == AlertLevel.CRITICAL else "⚠️ BAJO" if alert == AlertLevel.LOW else "✅ NORMAL"
            
            report += f"{item.product.code:<10} {item.product.name:<25} {item.product.category:<15} "
            report += f"{item.quantity:<8} {item.reserved_quantity:<8} {item.available_quantity:<8} {status:<12}\n"
        
        report += "=" * 100 + "\n"
        return report
    
    def export_csv(self, service: InventoryService, filename: str) -> None:
        items = service.get_all_inventory_items()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Reservado', 'Disponible', 'Estado'])
            for item in items:
                alert = item.get_alert_level()
                status = "CRÍTICO" if alert == AlertLevel.CRITICAL else "BAJO" if alert == AlertLevel.LOW else "NORMAL"
                writer.writerow([
                    item.product.code, item.product.name, item.product.category,
                    item.product.price, item.quantity, item.reserved_quantity,
                    item.available_quantity, status
                ])


class SalesAnalysisReport(ReportGenerator):
    """Reporte de análisis de ventas - productos más y menos vendidos"""
    
    def generate(self, service: InventoryService) -> str:
        most_sold = service.get_most_sold_products(10)
        least_sold = service.get_least_sold_products(10)
        
        report = "=" * 100 + "\n"
        report += " " * 30 + "REPORTE DE ANÁLISIS DE VENTAS\n"
        report += "=" * 100 + "\n\n"
        
        # Productos más vendidos
        report += "🔥 TOP 10 PRODUCTOS MÁS VENDIDOS\n"
        report += "-" * 100 + "\n"
        report += f"{'Posición':<10} {'Código':<12} {'Nombre':<35} {'Categoría':<20} {'Unidades':<15}\n"
        report += "-" * 100 + "\n"
        
        for i, (code, qty) in enumerate(most_sold, 1):
            product = service._product_repo.get(code)
            if product:
                report += f"#{i:<9} {code:<12} {product.name:<35} {product.category:<20} {qty:<15}\n"
        
        if not most_sold:
            report += "No hay datos de ventas disponibles\n"
        
        report += "\n"
        
        # Productos menos vendidos
        report += "📉 TOP 10 PRODUCTOS MENOS VENDIDOS\n"
        report += "-" * 100 + "\n"
        report += f"{'Posición':<10} {'Código':<12} {'Nombre':<35} {'Categoría':<20} {'Unidades':<15}\n"
        report += "-" * 100 + "\n"
        
        for i, (code, qty) in enumerate(least_sold, 1):
            product = service._product_repo.get(code)
            if product:
                report += f"#{i:<9} {code:<12} {product.name:<35} {product.category:<20} {qty:<15}\n"
        
        report += "\n"
        
        # Estadísticas generales
        total_exits = sum(m.quantity for m in service._movement_repo.get_by_type(MovementType.EXIT))
        total_entries = sum(m.quantity for m in service._movement_repo.get_by_type(MovementType.ENTRY))
        
        report += "📊 ESTADÍSTICAS GENERALES\n"
        report += "-" * 100 + "\n"
        report += f"Total de Salidas (Ventas): {total_exits} unidades\n"
        report += f"Total de Entradas: {total_entries} unidades\n"
        report += f"Movimientos Netos: {total_entries - total_exits} unidades\n"
        
        report += "=" * 100 + "\n"
        return report
    
    def export_csv(self, service: InventoryService, filename: str) -> None:
        most_sold = service.get_most_sold_products(10)
        least_sold = service.get_least_sold_products(10)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Más vendidos
            writer.writerow(['PRODUCTOS MÁS VENDIDOS'])
            writer.writerow(['Posición', 'Código', 'Nombre', 'Categoría', 'Unidades Vendidas'])
            for i, (code, qty) in enumerate(most_sold, 1):
                product = service._product_repo.get(code)
                if product:
                    writer.writerow([i, code, product.name, product.category, qty])
            
            writer.writerow([])
            
            # Menos vendidos
            writer.writerow(['PRODUCTOS MENOS VENDIDOS'])
            writer.writerow(['Posición', 'Código', 'Nombre', 'Categoría', 'Unidades Vendidas'])
            for i, (code, qty) in enumerate(least_sold, 1):
                product = service._product_repo.get(code)
                if product:
                    writer.writerow([i, code, product.name, product.category, qty])
    
    def export_pdf(self, service: InventoryService, filename: str) -> None:
        """Exportar análisis de ventas a PDF"""
        if not PDF_AVAILABLE:
            raise Exception("ReportLab no está instalado. Instale con: pip install reportlab")
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilo de título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Título
        title = Paragraph("REPORTE DE ANÁLISIS DE VENTAS", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Fecha
        date_text = f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Productos más vendidos
        most_sold = service.get_most_sold_products(10)
        
        elements.append(Paragraph("🔥 TOP 10 PRODUCTOS MÁS VENDIDOS", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        if most_sold:
            data = [['Pos.', 'Código', 'Nombre', 'Categoría', 'Unidades']]
            for i, (code, qty) in enumerate(most_sold, 1):
                product = service._product_repo.get(code)
                if product:
                    data.append([
                        str(i),
                        code,
                        product.name[:25],
                        product.category,
                        str(qty)
                    ])
            
            table = Table(data, colWidths=[0.5*inch, 1*inch, 2.5*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No hay datos de ventas disponibles", styles['Normal']))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Productos menos vendidos
        least_sold = service.get_least_sold_products(10)
        
        elements.append(Paragraph("📉 TOP 10 PRODUCTOS MENOS VENDIDOS", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        if least_sold:
            data = [['Pos.', 'Código', 'Nombre', 'Categoría', 'Unidades']]
            for i, (code, qty) in enumerate(least_sold, 1):
                product = service._product_repo.get(code)
                if product:
                    data.append([
                        str(i),
                        code,
                        product.name[:25],
                        product.category,
                        str(qty)
                    ])
            
            table = Table(data, colWidths=[0.5*inch, 1*inch, 2.5*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Estadísticas
        total_exits = sum(m.quantity for m in service._movement_repo.get_by_type(MovementType.EXIT))
        total_entries = sum(m.quantity for m in service._movement_repo.get_by_type(MovementType.ENTRY))
        
        elements.append(Paragraph("📊 ESTADÍSTICAS GENERALES", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        stats_data = [
            ['Concepto', 'Valor'],
            ['Total de Salidas (Ventas)', f'{total_exits} unidades'],
            ['Total de Entradas', f'{total_entries} unidades'],
            ['Movimientos Netos', f'{total_entries - total_exits} unidades']
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        
        # Generar PDF
        doc.build(elements)


class MovementsReport(ReportGenerator):
    """Reporte de movimientos de inventario"""
    
    def generate(self, service: InventoryService) -> str:
        movements = service._movement_repo.get_all()
        
        report = "=" * 110 + "\n"
        report += " " * 40 + "REPORTE DE MOVIMIENTOS\n"
        report += "=" * 110 + "\n\n"
        
        report += f"{'Fecha/Hora':<20} {'Código':<10} {'Tipo':<10} {'Cantidad':<10} {'Usuario':<15} {'Descripción':<35}\n"
        report += "-" * 110 + "\n"
        
        for mov in reversed(movements[-50:]):
            mov_type = "➕ ENTRADA" if mov.movement_type == MovementType.ENTRY else "➖ SALIDA"
            mov_dict = mov.to_dict()
            report += f"{mov_dict['timestamp']:<20} {mov.product_code:<10} {mov_type:<10} "
            report += f"{mov.quantity:<10} {mov.user:<15} {mov_dict['description']:<35}\n"
        
        report += "=" * 110 + "\n"
        return report
    
    def export_csv(self, service: InventoryService, filename: str) -> None:
        movements = service._movement_repo.get_all()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Fecha/Hora', 'Código', 'Tipo', 'Cantidad', 'Usuario', 'Descripción'])
            for mov in movements:
                mov_dict = mov.to_dict()
                mov_type = "ENTRADA" if mov.movement_type == MovementType.ENTRY else "SALIDA"
                writer.writerow([
                    mov_dict['timestamp'], mov.product_code, mov_type,
                    mov.quantity, mov.user, mov_dict['description']
                ])


class AlertsReport(ReportGenerator):
    """Reporte de alertas de stock"""
    
    def generate(self, service: InventoryService) -> str:
        critical = service.get_critical_stock_items()
        low = [item for item in service.get_low_stock_items() 
               if item.get_alert_level() == AlertLevel.LOW]
        
        report = "=" * 90 + "\n"
        report += " " * 30 + "REPORTE DE ALERTAS DE STOCK\n"
        report += "=" * 90 + "\n\n"
        
        report += "🔴 PRODUCTOS CRÍTICOS (< 25% del stock mínimo)\n"
        report += "-" * 90 + "\n"
        
        if critical:
            report += f"{'Código':<10} {'Nombre':<25} {'Stock':<10} {'Mínimo':<10} {'Porcentaje':<15}\n"
            report += "-" * 90 + "\n"
            for item in critical:
                report += f"{item.product.code:<10} {item.product.name:<25} {item.quantity:<10} "
                report += f"{item.product.min_stock:<10} {item.get_stock_percentage():<14.1f}%\n"
        else:
            report += "✅ No hay productos en estado crítico\n"
        
        report += "\n"
        
        report += "⚠️ PRODUCTOS CON STOCK BAJO\n"
        report += "-" * 90 + "\n"
        
        if low:
            report += f"{'Código':<10} {'Nombre':<25} {'Stock':<10} {'Mínimo':<10} {'Faltante':<15}\n"
            report += "-" * 90 + "\n"
            for item in low:
                diff = item.product.min_stock - item.quantity
                report += f"{item.product.code:<10} {item.product.name:<25} {item.quantity:<10} "
                report += f"{item.product.min_stock:<10} {diff:<15}\n"
        else:
            report += "✅ No hay productos con stock bajo\n"
        
        report += "=" * 90 + "\n"
        return report
    
    def export_csv(self, service: InventoryService, filename: str) -> None:
        items = service.get_low_stock_items()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Código', 'Nombre', 'Stock Actual', 'Stock Mínimo', 'Nivel de Alerta', 'Porcentaje'])
            for item in items:
                alert = "CRÍTICO" if item.get_alert_level() == AlertLevel.CRITICAL else "BAJO"
                writer.writerow([
                    item.product.code, item.product.name, item.quantity,
                    item.product.min_stock, alert, f"{item.get_stock_percentage():.1f}%"
                ])


class ValueReport(ReportGenerator):
    """Reporte de valorización del inventario"""
    
    def generate(self, service: InventoryService) -> str:
        items = service.get_all_inventory_items()
        
        report = "=" * 95 + "\n"
        report += " " * 30 + "REPORTE DE VALORIZACIÓN\n"
        report += "=" * 95 + "\n\n"
        
        report += f"{'Código':<10} {'Nombre':<25} {'Categoría':<15} {'Cantidad':<10} {'P.Unit':<12} {'Total':<15}\n"
        report += "-" * 95 + "\n"
        
        total_value = 0
        category_values = {}
        
        for item in sorted(items, key=lambda x: x.product.category):
            item_value = item.quantity * item.product.price
            total_value += item_value
            
            if item.product.category not in category_values:
                category_values[item.product.category] = 0
            category_values[item.product.category] += item_value
            
            report += f"{item.product.code:<10} {item.product.name:<25} {item.product.category:<15} "
            report += f"{item.quantity:<10} S/ {item.product.price:<11.2f} S/ {item_value:<14.2f}\n"
        
        report += "-" * 95 + "\n"
        report += f"{'VALOR TOTAL DEL INVENTARIO:':<70} S/ {total_value:,.2f}\n"
        report += "\n"
        
        report += "VALOR POR CATEGORÍA\n"
        report += "-" * 50 + "\n"
        for category, value in sorted(category_values.items(), key=lambda x: x[1], reverse=True):
            percentage = (value / total_value * 100) if total_value > 0 else 0
            report += f"{category:<30} S/ {value:>12,.2f} ({percentage:>5.1f}%)\n"
        
        report += "=" * 95 + "\n"
        return report
    
    def export_csv(self, service: InventoryService, filename: str) -> None:
        items = service.get_all_inventory_items()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Código', 'Nombre', 'Categoría', 'Cantidad', 'Precio Unitario', 'Valor Total'])
            for item in items:
                item_value = item.quantity * item.product.price
                writer.writerow([
                    item.product.code, item.product.name, item.product.category,
                    item.quantity, item.product.price, item_value
                ])


# ============= SCANNER DE CÓDIGO DE BARRAS =============

class BarcodeScanner:
    """Scanner de código de barras usando cámara"""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.is_scanning = False
        self.cap = None
    
    def start_scanning(self):
        """Iniciar escaneo"""
        if not BARCODE_AVAILABLE:
            raise Exception("Librerías de barcode no disponibles")
        
        self.is_scanning = True
        self.cap = cv2.VideoCapture(0)
        
        threading.Thread(target=self._scan_loop, daemon=True).start()
    
    def stop_scanning(self):
        """Detener escaneo"""
        self.is_scanning = False
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
    
    def _scan_loop(self):
        """Loop de escaneo"""
        while self.is_scanning:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Detectar códigos de barras
            barcodes = pyzbar.decode(frame)
            
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                
                # Dibujar rectángulo
                points = barcode.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    points = hull
                
                n = len(points)
                for j in range(n):
                    cv2.line(frame, tuple(points[j]), tuple(points[(j+1) % n]), (0, 255, 0), 3)
                
                # Mostrar datos
                cv2.putText(frame, barcode_data, (barcode.rect.left, barcode.rect.top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Callback
                self.callback(barcode_data)
                self.stop_scanning()
                return
            
            # Mostrar frame
            cv2.imshow('Scanner de Código de Barras - Presione ESC para salir', frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break
        
        self.stop_scanning()


# ============= PANTALLA DE LOGIN =============

class LoginWindow:
    """Ventana de login"""
    
    def __init__(self, on_success: Callable[[str], None]):
        self.on_success = on_success
        self.root = tk.Tk()
        self.root.title("Inicio de Sesión")
        self.root.geometry("450x350")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear widgets del login"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Logo
        tk.Label(main_frame, text="🏢", font=('Arial', 48), 
                bg='#2c3e50', fg='white').pack(pady=(0, 10))
        
        # Título
        tk.Label(main_frame, text="Sistema de Inventario",
                font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white').pack()
        
        tk.Label(main_frame, text="Ingrese sus credenciales",
                font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7').pack(pady=(5, 30))
        
        # Usuario
        user_frame = tk.Frame(main_frame, bg='#2c3e50')
        user_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(user_frame, text="👤", font=('Arial', 16),
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.username_entry = tk.Entry(user_frame, font=('Arial', 12), width=25)
        self.username_entry.pack(side=tk.LEFT, ipady=5)
        self.username_entry.insert(0, "Usuario")
        self.username_entry.bind('<FocusIn>', lambda e: self._on_entry_focus(self.username_entry, "Usuario"))
        self.username_entry.bind('<FocusOut>', lambda e: self._on_entry_unfocus(self.username_entry, "Usuario"))
        self.username_entry.config(fg='gray')
        
        # Contraseña
        pass_frame = tk.Frame(main_frame, bg='#2c3e50')
        pass_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(pass_frame, text="🔒", font=('Arial', 16),
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = tk.Entry(pass_frame, font=('Arial', 12), width=25, show='')
        self.password_entry.pack(side=tk.LEFT, ipady=5)
        self.password_entry.insert(0, "Contraseña")
        self.password_entry.bind('<FocusIn>', lambda e: self._on_password_focus())
        self.password_entry.bind('<FocusOut>', lambda e: self._on_password_unfocus())
        self.password_entry.config(fg='gray')
        
        # Bind Enter para login
        self.username_entry.bind('<Return>', lambda e: self._attempt_login())
        self.password_entry.bind('<Return>', lambda e: self._attempt_login())
        
        # Botón de login
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(pady=30)
        
        login_btn = tk.Button(btn_frame, text='Iniciar Sesión', font=('Arial', 12, 'bold'),
                             bg='#27ae60', fg='white', cursor='hand2',
                             command=self._attempt_login, padx=40, pady=10, bd=0)
        login_btn.pack()
        
        # Mensaje de ayuda
        tk.Label(main_frame, text="Usuario: admin | Contraseña: admin2025",
                font=('Arial', 8), bg='#2c3e50', fg='#7f8c8d').pack(pady=(20, 0))
    
    def _on_entry_focus(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    
    def _on_entry_unfocus(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='gray')
    
    def _on_password_focus(self):
        if self.password_entry.get() == "Contraseña":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show='*', fg='black')
    
    def _on_password_unfocus(self):
        if not self.password_entry.get():
            self.password_entry.config(show='')
            self.password_entry.insert(0, "Contraseña")
            self.password_entry.config(fg='gray')
    
    def _attempt_login(self):
        """Intentar login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in ["Usuario", ""] or password in ["Contraseña", ""]:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        # Validar credenciales
        if username == "admin" and password == "admin2025":
            self.root.destroy()
            self.on_success(username)
        else:
            messagebox.showerror("Error de Autenticación",
                               "Usuario o contraseña incorrectos\n\nUsuario: admin\nContraseña: admin2025")
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show='')
            self.password_entry.insert(0, "Contraseña")
            self.password_entry.config(fg='gray')
    
    def run(self):
        """Ejecutar ventana de login"""
        self.root.mainloop()


# ============= INTERFAZ GRÁFICA PROFESIONAL =============

class ModernButton(tk.Button):
    """Botón moderno con efectos hover"""
    
    def __init__(self, parent, **kwargs):
        self.default_bg = kwargs.get('bg', '#3498db')
        super().__init__(parent, **kwargs)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, e):
        self['background'] = self._lighten_color(self.default_bg)
    
    def _on_leave(self, e):
        self['background'] = self.default_bg
    
    def _lighten_color(self, color):
        colors = {
            '#3498db': '#5dade2',
            '#27ae60': '#52be80',
            '#e74c3c': '#ec7063',
            '#9b59b6': '#af7ac5',
            '#e67e22': '#f39c12',
            '#34495e': '#566573',
            '#16a085': '#1abc9c'
        }
        return colors.get(color, color)


class SearchFrame(tk.Frame):
    """Frame de búsqueda reutilizable"""
    
    def __init__(self, parent, on_search: Callable):
        super().__init__(parent, bg='white')
        self.on_search = on_search
        
        tk.Label(self, text="🔍 Buscar:", font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.on_search(self.search_var.get()))
        
        self.search_entry = tk.Entry(self, textvariable=self.search_var, font=('Arial', 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)


class StatisticsPanel(tk.Frame):
    """Panel de estadísticas en tiempo real"""
    
    def __init__(self, parent, service: InventoryService):
        super().__init__(parent, bg='#ecf0f1', relief=tk.RAISED, bd=2)
        self.service = service
        self._create_widgets()
        self.update_statistics()
    
    def _create_widgets(self):
        title = tk.Label(self, text="📊 ESTADÍSTICAS", font=('Arial', 12, 'bold'), 
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        self.stats_labels = {}
        stats_info = [
            ('productos', 'Total Productos:', '#3498db'),
            ('items', 'Total Items:', '#9b59b6'),
            ('valor', 'Valor Total:', '#27ae60'),
            ('bajo_stock', 'Stock Bajo:', '#e67e22'),
            ('critico', 'Críticos:', '#e74c3c')
        ]
        
        for key, text, color in stats_info:
            frame = tk.Frame(self, bg='#ecf0f1')
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(frame, text=text, font=('Arial', 9), bg='#ecf0f1', 
                    anchor='w').pack(side=tk.LEFT)
            
            label = tk.Label(frame, text="0", font=('Arial', 9, 'bold'), 
                           bg='#ecf0f1', fg=color, anchor='e')
            label.pack(side=tk.RIGHT)
            self.stats_labels[key] = label
    
    def update_statistics(self):
        stats = self.service.get_inventory_statistics()
        self.stats_labels['productos'].config(text=f"{stats['total_products']}")
        self.stats_labels['items'].config(text=f"{stats['total_items']}")
        self.stats_labels['valor'].config(text=f"S/ {stats['total_value']:,.2f}")
        self.stats_labels['bajo_stock'].config(text=f"{stats['low_stock_count']}")
        self.stats_labels['critico'].config(text=f"{stats['critical_stock_count']}")


class InventorySystemGUI:
    """Aplicación principal con interfaz profesional"""
    
    def __init__(self, root, username: str):
        self.root = root
        self.root.title("Sistema Profesional de Gestión de Inventarios")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilos
        self._configure_styles()
        
        # Inicializar servicios
        self.product_repo = ProductRepository()
        self.movement_repo = MovementRepository()
        self.service = InventoryService(self.product_repo, self.movement_repo)
        
        # Agregar observador para actualizar UI
        self.service.add_observer(self._on_inventory_changed)
        
        # Usuario actual
        self.current_user = username
        
        # Scanner de barcode
        self.barcode_scanner = None
        
        # Cargar datos de ejemplo
        self._load_sample_data()
        
        # Crear interfaz
        self._create_widgets()
    
    def _configure_styles(self):
        """Configurar estilos ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="white",
                       font=('Arial', 9))
        style.map('Treeview', background=[('selected', '#3498db')])
        
        style.configure("Treeview.Heading",
                       font=('Arial', 10, 'bold'),
                       background='#34495e',
                       foreground='white')
        
        style.configure('TNotebook', background='#f0f0f1')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[20, 10])
    
    def _load_sample_data(self):
        """Cargar datos de ejemplo"""
        try:
            products = [
                Product("TECH001", "Laptop Dell XPS 15", "Laptop profesional Core i7 16GB", 1299.99, 5, "Tecnología", "7501234567890"),
                Product("TECH002", "Mouse Logitech MX Master", "Mouse inalámbrico ergonómico", 99.99, 20, "Tecnología", "7501234567891"),
                Product("TECH003", "Teclado Mecánico Corsair", "Teclado RGB switches Cherry MX", 149.99, 10, "Tecnología", "7501234567892"),
                Product("OFF001", "Silla Ergonómica Herman Miller", "Silla oficina premium", 899.99, 3, "Oficina", "7501234567893"),
                Product("OFF002", "Escritorio Ajustable", "Escritorio eléctrico sit-stand", 599.99, 5, "Oficina", "7501234567894"),
                Product("ACC001", "Monitor LG 27 4K", "Monitor UltraHD IPS", 449.99, 8, "Accesorios", "7501234567895"),
                Product("ACC002", "Webcam Logitech C920", "Webcam Full HD 1080p", 79.99, 15, "Accesorios", "7501234567896"),
                Product("NET001", "Router TP-Link AX6000", "Router WiFi 6 Gigabit", 299.99, 6, "Redes", "7501234567897")
            ]
            
            for product in products:
                import random
                initial_qty = random.randint(product.min_stock, product.min_stock * 3)
                self.service.register_product(product, initial_qty, self.current_user)
            
            # Generar movimientos de ventas variados
            self.service.remove_stock("TECH002", 15, "Venta corporativa", self.current_user)
            self.service.remove_stock("TECH001", 2, "Venta cliente VIP", self.current_user)
            self.service.remove_stock("ACC002", 10, "Venta mayorista", self.current_user)
            self.service.remove_stock("TECH003", 8, "Venta online", self.current_user)
            self.service.add_stock("TECH001", 3, "Reposición proveedor", self.current_user)
            self.service.remove_stock("ACC001", 4, "Venta local", self.current_user)
            self.service.remove_stock("NET001", 1, "Venta individual", self.current_user)
            self.service.reserve_stock("OFF001", 1)
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def _create_widgets(self):
        """Crear widgets principales"""
        # Header
        self._create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel lateral de estadísticas
        self.stats_panel = StatisticsPanel(main_container, self.service)
        self.stats_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Notebook central
        notebook_container = tk.Frame(main_container, bg='#f0f0f0')
        notebook_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas
        self._create_products_tab()
        self._create_movements_tab()
        self._create_inventory_tab()
        self._create_reports_tab()
        self._create_analytics_tab()
        
        # Footer
        self._create_footer()
    
    def _create_header(self):
        """Crear header profesional"""
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header, bg='#2c3e50')
        title_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(title_frame, text="🏢", font=('Arial', 24), bg='#2c3e50').pack(side=tk.LEFT)
        
        text_frame = tk.Frame(title_frame, bg='#2c3e50')
        text_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(text_frame, text="Sistema de Gestión de Inventarios",
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(anchor='w')
        tk.Label(text_frame, text="Versión 3.0 Professional Edition",
                font=('Arial', 9), bg='#2c3e50', fg='#bdc3c7').pack(anchor='w')
        
        # Usuario y fecha
        info_frame = tk.Frame(header, bg='#2c3e50')
        info_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(info_frame, text=f"👤 Usuario: {self.current_user}",
                font=('Arial', 10), bg='#2c3e50', fg='white').pack(anchor='e')
        
        self.date_label = tk.Label(info_frame, text="", font=('Arial', 9),
                                   bg='#2c3e50', fg='#bdc3c7')
        self.date_label.pack(anchor='e')
        self._update_datetime()
    
    def _create_footer(self):
        """Crear footer"""
        footer = tk.Frame(self.root, bg='#34495e', height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        tk.Label(footer, text="© 2024 Sistema de Inventarios | Python & Tkinter",
                font=('Arial', 8), bg='#34495e', fg='#bdc3c7').pack(side=tk.LEFT, padx=10)
        
        tk.Label(footer, text="✓ Sistema Operativo",
                font=('Arial', 8), bg='#34495e', fg='#27ae60').pack(side=tk.RIGHT, padx=10)
    
    def _update_datetime(self):
        """Actualizar fecha y hora"""
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.date_label.config(text=f"📅 {now}")
        self.root.after(1000, self._update_datetime)
    
    def _create_products_tab(self):
        """Pestaña de gestión de productos"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text='📦 Productos')
        
        # Panel superior con formulario
        form_panel = tk.LabelFrame(frame, text="Registrar Nuevo Producto", 
                                   font=('Arial', 11, 'bold'), bg='white', padx=20, pady=15)
        form_panel.pack(fill=tk.X, padx=15, pady=15)
        
        # Grid de formulario
        fields_left = [
            ('Código*:', 'code'),
            ('Nombre*:', 'name'),
            ('Categoría*:', 'category'),
            ('Código Barras:', 'barcode')
        ]
        
        fields_right = [
            ('Precio (S/)*:', 'price'),
            ('Stock Mínimo*:', 'min_stock'),
            ('Cantidad Inicial*:', 'initial_qty')
        ]
        
        self.product_entries = {}
        
        # Columna izquierda
        left_frame = tk.Frame(form_panel, bg='white')
        left_frame.grid(row=0, column=0, padx=20, sticky='n')
        
        for i, (label_text, field_name) in enumerate(fields_left):
            tk.Label(left_frame, text=label_text, font=('Arial', 10), 
                    bg='white', anchor='w').grid(row=i, column=0, sticky='w', pady=8)
            
            if field_name == 'barcode':
                entry_frame = tk.Frame(left_frame, bg='white')
                entry_frame.grid(row=i, column=1, padx=10, pady=8, sticky='ew')
                
                entry = tk.Entry(entry_frame, font=('Arial', 10), width=18)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.product_entries[field_name] = entry
                
                if BARCODE_AVAILABLE:
                    scan_btn = tk.Button(entry_frame, text='📷', font=('Arial', 9),
                                        bg='#3498db', fg='white', cursor='hand2',
                                        command=lambda: self._scan_barcode_for_product())
                    scan_btn.pack(side=tk.LEFT, padx=(5, 0))
            else:
                entry = tk.Entry(left_frame, font=('Arial', 10), width=25)
                entry.grid(row=i, column=1, padx=10, pady=8)
                self.product_entries[field_name] = entry
        
        # Columna derecha
        right_frame = tk.Frame(form_panel, bg='white')
        right_frame.grid(row=0, column=1, padx=20, sticky='n')
        
        for i, (label_text, field_name) in enumerate(fields_right):
            tk.Label(right_frame, text=label_text, font=('Arial', 10),
                    bg='white', anchor='w').grid(row=i, column=0, sticky='w', pady=8)
            entry = tk.Entry(right_frame, font=('Arial', 10), width=25)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.product_entries[field_name] = entry
        
        # Descripción (ancho completo)
        desc_frame = tk.Frame(form_panel, bg='white')
        desc_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')
        
        tk.Label(desc_frame, text='Descripción*:', font=('Arial', 10),
                bg='white').pack(side=tk.LEFT, padx=5)
        self.product_entries['description'] = tk.Entry(desc_frame, font=('Arial', 10), width=70)
        self.product_entries['description'].pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Botones
        btn_frame = tk.Frame(form_panel, bg='white')
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ModernButton(btn_frame, text='✓ Registrar Producto', font=('Arial', 11, 'bold'),
                    bg='#27ae60', fg='white', cursor='hand2', command=self._register_product,
                    padx=25, pady=10).pack(side=tk.LEFT, padx=5)
        
        ModernButton(btn_frame, text='🗑️ Limpiar', font=('Arial', 11, 'bold'),
                    bg='#95a5a6', fg='white', cursor='hand2', command=self._clear_product_form,
                    padx=25, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Lista de productos
        list_panel = tk.LabelFrame(frame, text="Lista de Productos", 
                                   font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        list_panel.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Búsqueda
        SearchFrame(list_panel, self._search_products).pack(fill=tk.X, pady=5)
        
        # Treeview
        tree_frame = tk.Frame(list_panel, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.products_tree = ttk.Treeview(tree_frame,
            columns=('Código', 'Nombre', 'Categoría', 'Descripción', 'Precio', 'Stock Mín', 'Barcode'),
            show='headings', yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.products_tree.yview)
        hsb.config(command=self.products_tree.xview)
        
        for col, width in [('Código', 100), ('Nombre', 180), ('Categoría', 100),
                          ('Descripción', 220), ('Precio', 90), ('Stock Mín', 90), ('Barcode', 120)]:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._refresh_products_tree()
    
    def _scan_barcode_for_product(self):
        """Escanear código de barras para producto"""
        if not BARCODE_AVAILABLE:
            messagebox.showerror("Error", "Librerías de scanner no disponibles\nInstale: pip install opencv-python pyzbar")
            return
        
        def on_barcode_scanned(barcode):
            self.product_entries['barcode'].delete(0, tk.END)
            self.product_entries['barcode'].insert(0, barcode)
            messagebox.showinfo("Éxito", f"Código escaneado: {barcode}")
        
        try:
            self.barcode_scanner = BarcodeScanner(on_barcode_scanned)
            self.barcode_scanner.start_scanning()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar scanner: {str(e)}")
    
    def _create_movements_tab(self):
        """Pestaña de movimientos de stock"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text='📊 Movimientos')
        
        # Contenedor de formularios
        forms_container = tk.Frame(frame, bg='white')
        forms_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Entrada de stock
        entry_frame = tk.LabelFrame(forms_container, text="➕ Entrada de Stock",
                                    font=('Arial', 11, 'bold'), bg='white', fg='#27ae60',
                                    padx=20, pady=15)
        entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 7))
        
        tk.Label(entry_frame, text='Código del Producto:', font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=5)
        
        entry_code_frame = tk.Frame(entry_frame, bg='white')
        entry_code_frame.pack(fill=tk.X, pady=5)
        
        self.entry_code = tk.Entry(entry_code_frame, font=('Arial', 10), width=22)
        self.entry_code.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        if BARCODE_AVAILABLE:
            scan_btn = tk.Button(entry_code_frame, text='📷', font=('Arial', 9),
                                bg='#3498db', fg='white', cursor='hand2',
                                command=lambda: self._scan_barcode_for_entry())
            scan_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Label(entry_frame, text='Cantidad:', font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=5)
        self.entry_qty = tk.Entry(entry_frame, font=('Arial', 10), width=30)
        self.entry_qty.pack(fill=tk.X, pady=5)
        
        tk.Label(entry_frame, text='Descripción:', font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=5)
        self.entry_desc = tk.Entry(entry_frame, font=('Arial', 10), width=30)
        self.entry_desc.pack(fill=tk.X, pady=5)
        
        ModernButton(entry_frame, text='✓ Agregar Stock', font=('Arial', 10, 'bold'),
                    bg='#27ae60', fg='white', cursor='hand2', command=self._add_stock,
                    padx=20, pady=8).pack(pady=15)
        
        # Salida de stock
        exit_frame = tk.LabelFrame(forms_container, text="➖ Salida de Stock",
                                   font=('Arial', 11, 'bold'), bg='white', fg='#e74c3c',
                                   padx=20, pady=15)
        exit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(7, 0))
        
        tk.Label(exit_frame, text='Código del Producto:', font=('Arial', 10),
                bg='white').pack(anchor='w', pady=5)
        
        exit_code_frame = tk.Frame(exit_frame, bg='white')
        exit_code_frame.pack(fill=tk.X, pady=5)
        
        self.exit_code = tk.Entry(exit_code_frame, font=('Arial', 10), width=22)
        self.exit_code.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        if BARCODE_AVAILABLE:
            scan_btn = tk.Button(exit_code_frame, text='📷', font=('Arial', 9),
                                bg='#3498db', fg='white', cursor='hand2',
                                command=lambda: self._scan_barcode_for_exit())
            scan_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Label(exit_frame, text='Cantidad:', font=('Arial', 10),
                bg='white').pack(anchor='w', pady=5)
        self.exit_qty = tk.Entry(exit_frame, font=('Arial', 10), width=30)
        self.exit_qty.pack(fill=tk.X, pady=5)
        
        tk.Label(exit_frame, text='Descripción:', font=('Arial', 10),
                bg='white').pack(anchor='w', pady=5)
        self.exit_desc = tk.Entry(exit_frame, font=('Arial', 10), width=30)
        self.exit_desc.pack(fill=tk.X, pady=5)
        
        ModernButton(exit_frame, text='✓ Retirar Stock', font=('Arial', 10, 'bold'),
                    bg='#e74c3c', fg='white', cursor='hand2', command=self._remove_stock,
                    padx=20, pady=8).pack(pady=15)
        
        # Historial de movimientos
        history_panel = tk.LabelFrame(frame, text="Historial de Movimientos Recientes",
                                     font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        history_panel.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Botones de control
        control_frame = tk.Frame(history_panel, bg='white')
        control_frame.pack(fill=tk.X, pady=5)
        
        ModernButton(control_frame, text='🔄 Actualizar', font=('Arial', 9, 'bold'),
                    bg='#3498db', fg='white', cursor='hand2',
                    command=self._refresh_movements_tree,
                    padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(history_panel, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        
        self.movements_tree = ttk.Treeview(tree_frame,
            columns=('Fecha/Hora', 'Código', 'Tipo', 'Cantidad', 'Usuario', 'Descripción'),
            show='headings', yscrollcommand=vsb.set)
        
        vsb.config(command=self.movements_tree.yview)
        
        for col, width in [('Fecha/Hora', 160), ('Código', 100), ('Tipo', 100),
                          ('Cantidad', 100), ('Usuario', 120), ('Descripción', 300)]:
            self.movements_tree.heading(col, text=col)
            self.movements_tree.column(col, width=width)
        
        self.movements_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._refresh_movements_tree()
    
    def _scan_barcode_for_entry(self):
        """Escanear código de barras para entrada"""
        self._scan_barcode_generic(self.entry_code)
    
    def _scan_barcode_for_exit(self):
        """Escanear código de barras para salida"""
        self._scan_barcode_generic(self.exit_code)
    
    def _scan_barcode_generic(self, entry_widget):
        """Escanear código de barras genérico"""
        if not BARCODE_AVAILABLE:
            messagebox.showerror("Error", "Librerías de scanner no disponibles\nInstale: pip install opencv-python pyzbar")
            return
        
        def on_barcode_scanned(barcode):
            # Buscar producto por barcode
            product = self.product_repo.get_by_barcode(barcode)
            if product:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, product.code)
                messagebox.showinfo("Éxito", f"Producto encontrado:\n{product.name}\nCódigo: {product.code}")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró producto con barcode: {barcode}")
        
        try:
            self.barcode_scanner = BarcodeScanner(on_barcode_scanned)
            self.barcode_scanner.start_scanning()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar scanner: {str(e)}")
    
    def _create_inventory_tab(self):
        """Pestaña de inventario actual"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text='📋 Inventario')
        
        # Panel de control
        control_panel = tk.Frame(frame, bg='white')
        control_panel.pack(fill=tk.X, padx=15, pady=15)
        
        ModernButton(control_panel, text='🔄 Actualizar', font=('Arial', 10, 'bold'),
                    bg='#3498db', fg='white', cursor='hand2',
                    command=self._refresh_inventory_tree,
                    padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        ModernButton(control_panel, text='📤 Exportar CSV', font=('Arial', 10, 'bold'),
                    bg='#27ae60', fg='white', cursor='hand2',
                    command=self._export_inventory_csv,
                    padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Filtros
        tk.Label(control_panel, text='Filtrar por categoría:', font=('Arial', 10),
                bg='white').pack(side=tk.LEFT, padx=(20, 5))
        
        self.category_filter = ttk.Combobox(control_panel, font=('Arial', 10),
                                           state='readonly', width=15)
        self.category_filter.pack(side=tk.LEFT, padx=5)
        self.category_filter.bind('<<ComboboxSelected>>', lambda e: self._refresh_inventory_tree())
        
        # Búsqueda
        SearchFrame(control_panel, self._search_inventory).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.inventory_tree = ttk.Treeview(tree_frame,
            columns=('Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Reservado', 
                    'Disponible', 'Mínimo', '%', 'Estado'),
            show='headings', yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.inventory_tree.yview)
        hsb.config(command=self.inventory_tree.xview)
        
        columns_config = [
            ('Código', 100), ('Nombre', 200), ('Categoría', 120), ('Precio', 100),
            ('Stock', 80), ('Reservado', 80), ('Disponible', 80), ('Mínimo', 80),
            ('%', 80), ('Estado', 120)
        ]
        
        for col, width in columns_config:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=width)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configurar tags de colores
        self.inventory_tree.tag_configure('critical', background='#ffcccc')
        self.inventory_tree.tag_configure('low', background='#ffe6cc')
        self.inventory_tree.tag_configure('normal', background='white')
        
        self._update_category_filter()
        self._refresh_inventory_tree()
    
    def _create_reports_tab(self):
        """Pestaña de reportes"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text='📈 Reportes')
        
        # Panel de botones
        btn_panel = tk.Frame(frame, bg='white')
        btn_panel.pack(pady=20)
        
        reports = [
            ('📋 Inventario Completo', InventoryReport(), '#3498db'),
            ('📊 Movimientos', MovementsReport(), '#9b59b6'),
            ('⚠️ Alertas de Stock', AlertsReport(), '#e67e22'),
            ('💰 Valorización', ValueReport(), '#27ae60'),
            ('📈 Análisis de Ventas', SalesAnalysisReport(), '#16a085')
        ]
        
        row = 0
        col = 0
        for text, report_gen, color in reports:
            btn_frame = tk.Frame(btn_panel, bg='white')
            btn_frame.grid(row=row, column=col, padx=15, pady=10)
            
            ModernButton(btn_frame, text=text, font=('Arial', 11, 'bold'),
                        bg=color, fg='white', cursor='hand2',
                        command=lambda r=report_gen: self._show_report(r),
                        padx=30, pady=15, width=22).pack()
            
            btn_sub_frame = tk.Frame(btn_frame, bg='white')
            btn_sub_frame.pack(pady=5)
            
            ModernButton(btn_sub_frame, text='📤 CSV', font=('Arial', 8),
                        bg='#34495e', fg='white', cursor='hand2',
                        command=lambda r=report_gen: self._export_report_csv(r),
                        padx=10, pady=3).pack(side=tk.LEFT, padx=2)
            
            if PDF_AVAILABLE:
                ModernButton(btn_sub_frame, text='📄 PDF', font=('Arial', 8),
                            bg='#c0392b', fg='white', cursor='hand2',
                            command=lambda r=report_gen: self._export_report_pdf(r),
                            padx=10, pady=3).pack(side=tk.LEFT, padx=2)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Área de visualización
        view_frame = tk.LabelFrame(frame, text="Visualización de Reporte",
                                   font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        view_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Botones de control
        control_frame = tk.Frame(view_frame, bg='white')
        control_frame.pack(fill=tk.X, pady=5)
        
        ModernButton(control_frame, text='💾 Guardar TXT', font=('Arial', 9, 'bold'),
                    bg='#16a085', fg='white', cursor='hand2',
                    command=self._save_report_txt,
                    padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        ModernButton(control_frame, text='🗑️ Limpiar', font=('Arial', 9, 'bold'),
                    bg='#95a5a6', fg='white', cursor='hand2',
                    command=lambda: self.report_text.delete(1.0, tk.END),
                    padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # ScrolledText
        self.report_text = scrolledtext.ScrolledText(
            view_frame, font=('Courier New', 9), wrap=tk.WORD,
            bg='#2c3e50', fg='#ecf0f1', padx=15, pady=15,
            insertbackground='white'
        )
        self.report_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _create_analytics_tab(self):
        """Pestaña de analíticas y estadísticas"""
        frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame, text='📉 Analíticas')
        
        # Título
        tk.Label(frame, text="Panel de Análisis del Inventario",
                font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(pady=20)
        
        # Grid de métricas
        metrics_frame = tk.Frame(frame, bg='white')
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        stats = self.service.get_inventory_statistics()
        
        metrics = [
            ('📦 Total de Productos', stats['total_products'], '#3498db'),
            ('📊 Total de Items', stats['total_items'], '#9b59b6'),
            ('💰 Valor Total', f"S/ {stats['total_value']:,.2f}", '#27ae60'),
            ('⚠️ Stock Bajo', stats['low_stock_count'], '#e67e22'),
            ('🔴 Críticos', stats['critical_stock_count'], '#e74c3c'),
            ('📁 Categorías', stats['categories'], '#16a085')
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            card = tk.Frame(metrics_frame, bg=color, relief=tk.RAISED, bd=3)
            card.grid(row=i//3, column=i%3, padx=15, pady=15, sticky='nsew')
            
            tk.Label(card, text=label, font=('Arial', 12, 'bold'),
                    bg=color, fg='white').pack(pady=(20, 10))
            tk.Label(card, text=str(value), font=('Arial', 24, 'bold'),
                    bg=color, fg='white').pack(pady=(0, 20))
        
        for i in range(3):
            metrics_frame.columnconfigure(i, weight=1)
        
        # Botón de actualizar
        ModernButton(frame, text='🔄 Actualizar Analíticas', font=('Arial', 11, 'bold'),
                    bg='#3498db', fg='white', cursor='hand2',
                    command=self._refresh_analytics,
                    padx=30, pady=12).pack(pady=20)
    
    # ============= MÉTODOS DE ACCIONES =============
    
    def _register_product(self):
        """Registrar nuevo producto"""
        try:
            code = self.product_entries['code'].get().strip().upper()
            name = self.product_entries['name'].get().strip()
            category = self.product_entries['category'].get().strip()
            description = self.product_entries['description'].get().strip()
            price = float(self.product_entries['price'].get())
            min_stock = int(self.product_entries['min_stock'].get())
            initial_qty = int(self.product_entries['initial_qty'].get())
            barcode = self.product_entries['barcode'].get().strip()
            
            product = Product(code, name, description, price, min_stock, category, barcode)
            self.service.register_product(product, initial_qty, self.current_user)
            
            self._clear_product_form()
            messagebox.showinfo("Éxito", f"✓ Producto {code} registrado correctamente")
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def _clear_product_form(self):
        """Limpiar formulario de productos"""
        for entry in self.product_entries.values():
            entry.delete(0, tk.END)
    
    def _add_stock(self):
        """Agregar stock"""
        try:
            code = self.entry_code.get().strip().upper()
            quantity = int(self.entry_qty.get())
            description = self.entry_desc.get().strip()
            
            self.service.add_stock(code, quantity, description, self.current_user)
            
            self.entry_code.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
            
            messagebox.showinfo("Éxito", f"✓ Stock agregado correctamente\n+{quantity} unidades")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _remove_stock(self):
        """Retirar stock"""
        try:
            code = self.exit_code.get().strip().upper()
            quantity = int(self.exit_qty.get())
            description = self.exit_desc.get().strip()
            
            self.service.remove_stock(code, quantity, description, self.current_user)
            
            self.exit_code.delete(0, tk.END)
            self.exit_qty.delete(0, tk.END)
            self.exit_desc.delete(0, tk.END)
            
            messagebox.showinfo("Éxito", f"✓ Stock retirado correctamente\n-{quantity} unidades")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _search_products(self, query: str):
        """Buscar productos"""
        self._refresh_products_tree(query)
    
    def _search_inventory(self, query: str):
        """Buscar en inventario"""
        self._refresh_inventory_tree(query)
    
    def _refresh_products_tree(self, search_query: str = ""):
        """Actualizar árbol de productos"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        if search_query:
            products = self.product_repo.search(search_query)
        else:
            products = self.product_repo.get_all()
        
        for product in sorted(products, key=lambda p: p.code):
            values = (
                product.code,
                product.name,
                product.category,
                product.description,
                f"S/ {product.price:.2f}",
                product.min_stock,
                product.barcode or "N/A"
            )
            self.products_tree.insert('', tk.END, values=values)
    
    def _refresh_movements_tree(self):
        """Actualizar árbol de movimientos"""
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        
        movements = self.service._movement_repo.get_all()
        
        for mov in reversed(movements[-100:]):
            mov_dict = mov.to_dict()
            mov_type = "➕ ENTRADA" if mov.movement_type == MovementType.ENTRY else "➖ SALIDA"
            
            values = (
                mov_dict['timestamp'],
                mov.product_code,
                mov_type,
                mov.quantity,
                mov.user,
                mov_dict['description']
            )
            
            tag = 'entry' if mov.movement_type == MovementType.ENTRY else 'exit'
            self.movements_tree.insert('', tk.END, values=values, tags=(tag,))
        
        self.movements_tree.tag_configure('entry', foreground='#27ae60')
        self.movements_tree.tag_configure('exit', foreground='#e74c3c')
    
    def _update_category_filter(self):
        """Actualizar filtro de categorías"""
        categories = ['Todas'] + self.product_repo.get_categories()
        self.category_filter['values'] = categories
        self.category_filter.set('Todas')
    
    def _refresh_inventory_tree(self, search_query: str = ""):
        """Actualizar árbol de inventario"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        items = self.service.get_all_inventory_items()
        
        category_filter = self.category_filter.get()
        if category_filter and category_filter != 'Todas':
            items = [item for item in items if item.product.category == category_filter]
        
        if search_query:
            query_lower = search_query.lower()
            items = [item for item in items 
                    if query_lower in item.product.code.lower() or 
                       query_lower in item.product.name.lower()]
        
        for item in sorted(items, key=lambda x: x.product.code):
            alert = item.get_alert_level()
            
            if alert == AlertLevel.CRITICAL:
                status = "🔴 CRÍTICO"
                tag = 'critical'
            elif alert == AlertLevel.LOW:
                status = "⚠️ BAJO"
                tag = 'low'
            else:
                status = "✅ NORMAL"
                tag = 'normal'
            
            values = (
                item.product.code,
                item.product.name,
                item.product.category,
                f"S/ {item.product.price:.2f}",
                item.quantity,
                item.reserved_quantity,
                item.available_quantity,
                item.product.min_stock,
                f"{item.get_stock_percentage():.1f}%",
                status
            )
            
            self.inventory_tree.insert('', tk.END, values=values, tags=(tag,))
    
    def _show_report(self, report_generator: ReportGenerator):
        """Mostrar reporte"""
        try:
            report = report_generator.generate(self.service)
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, report)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def _export_report_csv(self, report_generator: ReportGenerator):
        """Exportar reporte a CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                report_generator.export_csv(self.service, filename)
                messagebox.showinfo("Éxito", f"✓ Reporte exportado a:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _export_report_pdf(self, report_generator: ReportGenerator):
        """Exportar reporte a PDF"""
        try:
            if not PDF_AVAILABLE:
                messagebox.showerror("Error", "ReportLab no está instalado.\nInstale con: pip install reportlab")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                report_generator.export_pdf(self.service, filename)
                messagebox.showinfo("Éxito", f"✓ Reporte PDF exportado a:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")
    
    def _export_inventory_csv(self):
        """Exportar inventario completo a CSV"""
        self._export_report_csv(InventoryReport())
    
    def _save_report_txt(self):
        """Guardar reporte como TXT"""
        try:
            content = self.report_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Advertencia", "No hay reporte para guardar")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Éxito", f"✓ Reporte guardado en:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _refresh_analytics(self):
        """Refrescar analíticas"""
        for i, tab in enumerate(self.notebook.tabs()):
            if self.notebook.tab(i, "text") == '📉 Analíticas':
                self.notebook.forget(i)
                break
        self._create_analytics_tab()
        messagebox.showinfo("Actualizado", "✓ Analíticas actualizadas")
    
    def _on_inventory_changed(self):
        """Callback cuando cambia el inventario"""
        self.stats_panel.update_statistics()
        self._update_category_filter()
        self._refresh_products_tree()
        self._refresh_inventory_tree()
        self._refresh_movements_tree()


# ============= PUNTO DE ENTRADA =============

def main():
    """Iniciar la aplicación"""
    
    # Verificar dependencias
    warnings = []
    if not PDF_AVAILABLE:
        warnings.append("⚠️ ReportLab no instalado - No se podrán generar PDFs\n   Instale con: pip install reportlab")
    if not BARCODE_AVAILABLE:
        warnings.append("⚠️ Librerías de barcode no instaladas - Scanner no disponible\n   Instale con: pip install opencv-python pyzbar")
    
    if warnings:
        print("\n" + "="*70)
        print("ADVERTENCIAS DE DEPENDENCIAS")
        print("="*70)
        for warning in warnings:
            print(warning)
        print("="*70 + "\n")
    
    # Mostrar login
    def on_login_success(username):
        root = tk.Tk()
        
        # Centrar ventana
        root.update_idletasks()
        width = 1400
        height = 800
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        app = InventorySystemGUI(root, username)
        
        # Mensaje de bienvenida
        welcome_msg = f"Bienvenido {username}!\n\n"
        welcome_msg += "Sistema de Gestión de Inventarios v3.0\n\n"
        welcome_msg += "✓ Sistema cargado con datos de ejemplo\n"
        welcome_msg += "✓ Todas las funciones operativas\n"
        welcome_msg += "✓ Reporte de análisis de ventas disponible\n"
        
        if PDF_AVAILABLE:
            welcome_msg += "✓ Exportación a PDF habilitada\n"
        else:
            welcome_msg += "⚠️ Exportación a PDF no disponible (instale reportlab)\n"
        
        if BARCODE_AVAILABLE:
            welcome_msg += "✓ Scanner de código de barras habilitado\n"
        else:
            welcome_msg += "⚠️ Scanner no disponible (instale opencv-python y pyzbar)\n"
        
        welcome_msg += "\n¡Comience a gestionar su inventario!"
        
        messagebox.showinfo("Bienvenido", welcome_msg)
        
        root.mainloop()
    
    # Iniciar con login
    login = LoginWindow(on_login_success)
    login.run()


if __name__ == "__main__":
    main()
