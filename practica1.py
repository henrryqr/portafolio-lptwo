import json
import csv
from datetime import datetime
import os
import random


# ============= CLASES  =============

class Producto:
    """Modelo de producto"""
    
    def __init__(self, codigo, nombre, descripcion, precio, stock_minimo, categoria="General", codigo_barras=""):
        self.codigo = codigo.upper()
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock_minimo = stock_minimo
        self.categoria = categoria
        self.codigo_barras = codigo_barras
        
        # Validaciones básicas
        if not self.codigo or not self.nombre:
            raise ValueError("Código y nombre son obligatorios")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock_minimo': self.stock_minimo,
            'categoria': self.categoria,
            'codigo_barras': self.codigo_barras
        }
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre} (S/{self.precio:.2f})"


class MovimientoStock:
    """Modelo de movimiento de stock"""
    
    def __init__(self, codigo_producto, cantidad, tipo_movimiento, descripcion="", usuario="Sistema"):
        self.codigo_producto = codigo_producto.upper()
        self.cantidad = cantidad
        self.tipo_movimiento = tipo_movimiento  # "entrada" o "salida"
        self.descripcion = descripcion
        self.usuario = usuario
        self.fecha_hora = datetime.now()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'codigo_producto': self.codigo_producto,
            'cantidad': self.cantidad,
            'tipo_movimiento': self.tipo_movimiento,
            'descripcion': self.descripcion,
            'usuario': self.usuario,
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
        }


class ItemInventario:
    """Gestión de stock de un producto"""
    
    def __init__(self, producto, cantidad=0):
        self.producto = producto
        self.cantidad = cantidad
        self.cantidad_reservada = 0
    
    def get_cantidad_disponible(self):
        """Cantidad disponible (total - reservado)"""
        return self.cantidad - self.cantidad_reservada
    
    def agregar_stock(self, cantidad):
        """Agregar stock"""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self.cantidad += cantidad
    
    def retirar_stock(self, cantidad):
        """Retirar stock"""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if cantidad > self.get_cantidad_disponible():
            raise ValueError(f"Stock insuficiente. Disponible: {self.get_cantidad_disponible()}")
        self.cantidad -= cantidad
    
    def reservar_stock(self, cantidad):
        """Reservar stock para pedidos"""
        if cantidad > self.get_cantidad_disponible():
            raise ValueError(f"No hay suficiente stock disponible para reservar")
        self.cantidad_reservada += cantidad
    
    def get_nivel_alerta(self):
        """Determinar el nivel de alerta del stock"""
        if self.cantidad < (self.producto.stock_minimo * 0.25):
            return "CRITICO"
        elif self.cantidad < self.producto.stock_minimo:
            return "BAJO"
        return "NORMAL"
    
    def get_porcentaje_stock(self):
        """Porcentaje del stock respecto al mínimo"""
        if self.producto.stock_minimo == 0:
            return 100.0
        return (self.cantidad / self.producto.stock_minimo) * 100
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'producto': self.producto.to_dict(),
            'cantidad': self.cantidad,
            'cantidad_disponible': self.get_cantidad_disponible(),
            'cantidad_reservada': self.cantidad_reservada,
            'nivel_alerta': self.get_nivel_alerta(),
            'porcentaje_stock': self.get_porcentaje_stock()
        }


# ============= REPOSITORIOS =============

class RepositorioProductos:
    """Gestión de productos"""
    
    def __init__(self):
        self.productos = {}  # {codigo: Producto}
    
    def agregar(self, producto):
        """Agregar producto"""
        if self.existe(producto.codigo):
            raise ValueError(f"El producto {producto.codigo} ya existe")
        self.productos[producto.codigo] = producto
    
    def obtener(self, codigo):
        """Obtener producto por código"""
        return self.productos.get(codigo.upper())
    
    def obtener_por_codigo_barras(self, codigo_barras):
        """Buscar producto por código de barras"""
        for producto in self.productos.values():
            if producto.codigo_barras == codigo_barras:
                return producto
        return None
    
    def obtener_todos(self):
        """Obtener todos los productos"""
        return list(self.productos.values())
    
    def actualizar(self, codigo, producto):
        """Actualizar producto"""
        if not self.existe(codigo):
            raise ValueError(f"El producto {codigo} no existe")
        self.productos[codigo] = producto
    
    def eliminar(self, codigo):
        """Eliminar producto"""
        if codigo in self.productos:
            del self.productos[codigo]
    
    def existe(self, codigo):
        """Verificar si existe producto"""
        return codigo.upper() in self.productos
    
    def buscar(self, texto):
        """Buscar productos por código o nombre"""
        texto = texto.lower()
        resultados = []
        for producto in self.productos.values():
            if texto in producto.codigo.lower() or texto in producto.nombre.lower():
                resultados.append(producto)
        return resultados
    
    def obtener_por_categoria(self, categoria):
        """Obtener productos por categoría"""
        return [p for p in self.productos.values() if p.categoria == categoria]
    
    def obtener_categorias(self):
        """Obtener todas las categorías únicas"""
        categorias = set()
        for producto in self.productos.values():
            categorias.add(producto.categoria)
        return list(categorias)


class RepositorioMovimientos:
    """Gestión de movimientos de stock"""
    
    def __init__(self):
        self.movimientos = []
    
    def agregar(self, movimiento):
        """Agregar movimiento"""
        self.movimientos.append(movimiento)
    
    def obtener_todos(self):
        """Obtener todos los movimientos"""
        return self.movimientos.copy()
    
    def obtener_por_producto(self, codigo_producto):
        """Obtener movimientos de un producto específico"""
        return [m for m in self.movimientos if m.codigo_producto == codigo_producto.upper()]
    
    def obtener_por_tipo(self, tipo_movimiento):
        """Obtener movimientos por tipo"""
        return [m for m in self.movimientos if m.tipo_movimiento == tipo_movimiento]
    
    def obtener_por_rango_fechas(self, fecha_inicio, fecha_fin):
        """Obtener movimientos en un rango de fechas"""
        return [m for m in self.movimientos 
                if fecha_inicio <= m.fecha_hora <= fecha_fin]


# ============= SERVICIO DE INVENTARIO =============

class ServicioInventario:
    """Servicio principal de gestión de inventario"""
    
    def __init__(self, repositorio_productos, repositorio_movimientos):
        self.repositorio_productos = repositorio_productos
        self.repositorio_movimientos = repositorio_movimientos
        self.inventario = {}  # {codigo: ItemInventario}
    
    def registrar_producto(self, producto, cantidad_inicial=0, usuario="Sistema"):
        """Registrar un nuevo producto"""
        if self.repositorio_productos.existe(producto.codigo):
            raise ValueError(f"El producto {producto.codigo} ya existe")
        
        self.repositorio_productos.agregar(producto)
        self.inventario[producto.codigo] = ItemInventario(producto, cantidad_inicial)
        
        if cantidad_inicial > 0:
            movimiento = MovimientoStock(
                producto.codigo, cantidad_inicial, "entrada", "Stock inicial", usuario
            )
            self.repositorio_movimientos.agregar(movimiento)
    
    def agregar_stock(self, codigo_producto, cantidad, descripcion="", usuario="Sistema"):
        """Agregar stock a un producto"""
        if codigo_producto not in self.inventario:
            raise ValueError(f"Producto {codigo_producto} no encontrado")
        
        self.inventario[codigo_producto].agregar_stock(cantidad)
        movimiento = MovimientoStock(codigo_producto, cantidad, "entrada", descripcion, usuario)
        self.repositorio_movimientos.agregar(movimiento)
    
    def retirar_stock(self, codigo_producto, cantidad, descripcion="", usuario="Sistema"):
        """Retirar stock de un producto"""
        if codigo_producto not in self.inventario:
            raise ValueError(f"Producto {codigo_producto} no encontrado")
        
        self.inventario[codigo_producto].retirar_stock(cantidad)
        movimiento = MovimientoStock(codigo_producto, cantidad, "salida", descripcion, usuario)
        self.repositorio_movimientos.agregar(movimiento)
    
    def reservar_stock(self, codigo_producto, cantidad):
        """Reservar stock para pedidos"""
        if codigo_producto not in self.inventario:
            raise ValueError(f"Producto {codigo_producto} no encontrado")
        
        self.inventario[codigo_producto].reservar_stock(cantidad)
    
    def obtener_item_inventario(self, codigo_producto):
        """Obtener item de inventario"""
        return self.inventario.get(codigo_producto.upper())
    
    def obtener_todos_items(self):
        """Obtener todos los items del inventario"""
        return list(self.inventario.values())
    
    def obtener_items_stock_bajo(self):
        """Obtener productos con stock bajo"""
        items_bajo = []
        for item in self.inventario.values():
            if item.get_nivel_alerta() != "NORMAL":
                items_bajo.append(item)
        return items_bajo
    
    def obtener_items_stock_critico(self):
        """Obtener productos con stock crítico"""
        items_critico = []
        for item in self.inventario.values():
            if item.get_nivel_alerta() == "CRITICO":
                items_critico.append(item)
        return items_critico
    
    def get_valor_total_inventario(self):
        """Calcular valor total del inventario"""
        total = 0
        for item in self.inventario.values():
            total += item.cantidad * item.producto.precio
        return total
    
    def get_estadisticas(self):
        """Obtener estadísticas del inventario"""
        items = list(self.inventario.values())
        items_bajo = self.obtener_items_stock_bajo()
        items_critico = self.obtener_items_stock_critico()
        
        return {
            'total_productos': len(items),
            'total_items': sum(item.cantidad for item in items),
            'valor_total': self.get_valor_total_inventario(),
            'stock_bajo_count': len(items_bajo),
            'stock_critico_count': len(items_critico),
            'categorias': len(self.repositorio_productos.obtener_categorias())
        }
    
    def obtener_productos_mas_vendidos(self, limite=10):
        """Obtener productos más vendidos"""
        ventas = {}
        
        # Contar ventas por producto
        for movimiento in self.repositorio_movimientos.obtener_todos():
            if movimiento.tipo_movimiento == "salida":
                if movimiento.codigo_producto not in ventas:
                    ventas[movimiento.codigo_producto] = 0
                ventas[movimiento.codigo_producto] += movimiento.cantidad
        
        # Ordenar de mayor a menor
        return sorted(ventas.items(), key=lambda x: x[1], reverse=True)[:limite]
    
    def obtener_productos_menos_vendidos(self, limite=10):
        """Obtener productos menos vendidos"""
        ventas = {}
        
        # Inicializar todos los productos con 0 ventas
        for codigo in self.inventario.keys():
            ventas[codigo] = 0
        
        # Contar ventas reales
        for movimiento in self.repositorio_movimientos.obtener_todos():
            if movimiento.tipo_movimiento == "salida":
                ventas[movimiento.codigo_producto] += movimiento.cantidad
        
        # Ordenar de menor a mayor
        return sorted(ventas.items(), key=lambda x: x[1])[:limite]


# ============= GENERADORES DE REPORTES =============

class ReporteInventario:
    """Reporte completo de inventario"""
    
    def generar(self, servicio):
        """Generar reporte de inventario"""
        items = servicio.obtener_todos_items()
        estadisticas = servicio.get_estadisticas()
        
        reporte = "=" * 100 + "\n"
        reporte += " " * 35 + "REPORTE DE INVENTARIO ACTUAL\n"
        reporte += "=" * 100 + "\n\n"
        
        reporte += f"Total de Productos: {estadisticas['total_productos']}\n"
        reporte += f"Total de Items: {estadisticas['total_items']}\n"
        reporte += f"Valor Total: S/ {estadisticas['valor_total']:,.2f}\n"
        reporte += f"Productos con Stock Bajo: {estadisticas['stock_bajo_count']}\n"
        reporte += f"Productos Críticos: {estadisticas['stock_critico_count']}\n\n"
        
        reporte += "-" * 100 + "\n"
        reporte += f"{'Código':<10} {'Nombre':<25} {'Categoría':<15} {'Stock':<8} {'Disp.':<8} {'Estado':<12}\n"
        reporte += "-" * 100 + "\n"
        
        for item in sorted(items, key=lambda x: x.producto.codigo):
            nivel = item.get_nivel_alerta()
            estado = "CRÍTICO" if nivel == "CRITICO" else "BAJO" if nivel == "BAJO" else "NORMAL"
            
            reporte += f"{item.producto.codigo:<10} {item.producto.nombre:<25} {item.producto.categoria:<15} "
            reporte += f"{item.cantidad:<8} {item.get_cantidad_disponible():<8} {estado:<12}\n"
        
        reporte += "=" * 100 + "\n"
        return reporte
    
    def exportar_csv(self, servicio, nombre_archivo):
        """Exportar a CSV"""
        items = servicio.obtener_todos_items()
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Disponible', 'Estado'])
            for item in items:
                nivel = item.get_nivel_alerta()
                estado = "CRÍTICO" if nivel == "CRITICO" else "BAJO" if nivel == "BAJO" else "NORMAL"
                writer.writerow([
                    item.producto.codigo, item.producto.nombre, item.producto.categoria,
                    item.producto.precio, item.cantidad, item.get_cantidad_disponible(), estado
                ])


class ReporteMovimientos:
    """Reporte de movimientos de inventario"""
    
    def generar(self, servicio):
        """Generar reporte de movimientos"""
        movimientos = servicio.repositorio_movimientos.obtener_todos()
        
        reporte = "=" * 110 + "\n"
        reporte += " " * 40 + "REPORTE DE MOVIMIENTOS\n"
        reporte += "=" * 110 + "\n\n"
        
        reporte += f"{'Fecha/Hora':<20} {'Código':<10} {'Tipo':<10} {'Cantidad':<10} {'Usuario':<15} {'Descripción':<35}\n"
        reporte += "-" * 110 + "\n"
        
        # Mostrar últimos 50 movimientos
        for mov in reversed(movimientos[-50:]):
            tipo = "ENTRADA" if mov.tipo_movimiento == "entrada" else "SALIDA"
            reporte += f"{mov.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'):<20} "
            reporte += f"{mov.codigo_producto:<10} {tipo:<10} {mov.cantidad:<10} "
            reporte += f"{mov.usuario:<15} {mov.descripcion:<35}\n"
        
        reporte += "=" * 110 + "\n"
        return reporte
    
    def exportar_csv(self, servicio, nombre_archivo):
        """Exportar a CSV"""
        movimientos = servicio.repositorio_movimientos.obtener_todos()
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Fecha/Hora', 'Código', 'Tipo', 'Cantidad', 'Usuario', 'Descripción'])
            for mov in movimientos:
                writer.writerow([
                    mov.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    mov.codigo_producto,
                    "ENTRADA" if mov.tipo_movimiento == "entrada" else "SALIDA",
                    mov.cantidad,
                    mov.usuario,
                    mov.descripcion
                ])


class ReporteAlertas:
    """Reporte de alertas de stock"""
    
    def generar(self, servicio):
        """Generar reporte de alertas"""
        items_criticos = servicio.obtener_items_stock_critico()
        items_bajo = [item for item in servicio.obtener_items_stock_bajo() 
                     if item.get_nivel_alerta() == "BAJO"]
        
        reporte = "=" * 90 + "\n"
        reporte += " " * 30 + "REPORTE DE ALERTAS DE STOCK\n"
        reporte += "=" * 90 + "\n\n"
        
        # Productos críticos
        reporte += "PRODUCTOS CRÍTICOS (< 25% del stock mínimo)\n"
        reporte += "-" * 90 + "\n"
        
        if items_criticos:
            reporte += f"{'Código':<10} {'Nombre':<25} {'Stock':<10} {'Mínimo':<10} {'Porcentaje':<15}\n"
            reporte += "-" * 90 + "\n"
            for item in items_criticos:
                reporte += f"{item.producto.codigo:<10} {item.producto.nombre:<25} {item.cantidad:<10} "
                reporte += f"{item.producto.stock_minimo:<10} {item.get_porcentaje_stock():<14.1f}%\n"
        else:
            reporte += "No hay productos en estado crítico\n"
        
        reporte += "\n"
        
        # Productos con stock bajo
        reporte += "PRODUCTOS CON STOCK BAJO\n"
        reporte += "-" * 90 + "\n"
        
        if items_bajo:
            reporte += f"{'Código':<10} {'Nombre':<25} {'Stock':<10} {'Mínimo':<10} {'Faltante':<15}\n"
            reporte += "-" * 90 + "\n"
            for item in items_bajo:
                faltante = item.producto.stock_minimo - item.cantidad
                reporte += f"{item.producto.codigo:<10} {item.producto.nombre:<25} {item.cantidad:<10} "
                reporte += f"{item.producto.stock_minimo:<10} {faltante:<15}\n"
        else:
            reporte += "No hay productos con stock bajo\n"
        
        reporte += "=" * 90 + "\n"
        return reporte


class ReporteValorizacion:
    """Reporte de valorización del inventario"""
    
    def generar(self, servicio):
        """Generar reporte de valorización"""
        items = servicio.obtener_todos_items()
        
        reporte = "=" * 95 + "\n"
        reporte += " " * 30 + "REPORTE DE VALORIZACIÓN\n"
        reporte += "=" * 95 + "\n\n"
        
        reporte += f"{'Código':<10} {'Nombre':<25} {'Categoría':<15} {'Cantidad':<10} {'P.Unit':<12} {'Total':<15}\n"
        reporte += "-" * 95 + "\n"
        
        valor_total = 0
        valores_categoria = {}
        
        for item in sorted(items, key=lambda x: x.producto.categoria):
            valor_item = item.cantidad * item.producto.precio
            valor_total += valor_item
            
            if item.producto.categoria not in valores_categoria:
                valores_categoria[item.producto.categoria] = 0
            valores_categoria[item.producto.categoria] += valor_item
            
            reporte += f"{item.producto.codigo:<10} {item.producto.nombre:<25} {item.producto.categoria:<15} "
            reporte += f"{item.cantidad:<10} S/ {item.producto.precio:<11.2f} S/ {valor_item:<14.2f}\n"
        
        reporte += "-" * 95 + "\n"
        reporte += f"{'VALOR TOTAL DEL INVENTARIO:':<70} S/ {valor_total:,.2f}\n"
        reporte += "\n"
        
        reporte += "VALOR POR CATEGORÍA\n"
        reporte += "-" * 50 + "\n"
        for categoria, valor in sorted(valores_categoria.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (valor / valor_total * 100) if valor_total > 0 else 0
            reporte += f"{categoria:<30} S/ {valor:>12,.2f} ({porcentaje:>5.1f}%)\n"
        
        reporte += "=" * 95 + "\n"
        return reporte


# ============= SISTEMA DE PERSISTENCIA =============

class GestorDatos:
    """Gestor de persistencia de datos"""
    
    def guardar_datos(self, servicio, nombre_archivo="inventario_datos.json"):
        """Guardar todo el sistema en un archivo JSON"""
        datos = {
            'productos': [p.to_dict() for p in servicio.repositorio_productos.obtener_todos()],
            'movimientos': [m.to_dict() for m in servicio.repositorio_movimientos.obtener_todos()],
            'inventario': {codigo: item.to_dict() for codigo, item in servicio.inventario.items()}
        }
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def cargar_datos(self, servicio, nombre_archivo="inventario_datos.json"):
        """Cargar datos desde un archivo JSON"""
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Limpiar datos actuales
            servicio.repositorio_productos.productos.clear()
            servicio.inventario.clear()
            servicio.repositorio_movimientos.movimientos.clear()
            
            # Cargar productos
            for producto_data in datos.get('productos', []):
                producto = Producto(**producto_data)
                servicio.repositorio_productos.agregar(producto)
            
            # Cargar inventario
            for codigo, item_data in datos.get('inventario', {}).items():
                producto = servicio.repositorio_productos.obtener(codigo)
                if producto:
                    item = ItemInventario(producto, item_data['cantidad'])
                    item.cantidad_reservada = item_data['cantidad_reservada']
                    servicio.inventario[codigo] = item
            
            # Cargar movimientos
            for movimiento_data in datos.get('movimientos', []):
                movimiento = MovimientoStock(
                    movimiento_data['codigo_producto'],
                    movimiento_data['cantidad'],
                    movimiento_data['tipo_movimiento'],
                    movimiento_data['descripcion'],
                    movimiento_data['usuario']
                )
                movimiento.fecha_hora = datetime.strptime(movimiento_data['fecha_hora'], '%Y-%m-%d %H:%M:%S')
                servicio.repositorio_movimientos.agregar(movimiento)
            
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False


# ============= INTERFAZ DE CONSOLA =============

class SistemaInventarioConsola:
    """Sistema de inventario por consola"""
    
    def __init__(self):
        self.repositorio_productos = RepositorioProductos()
        self.repositorio_movimientos = RepositorioMovimientos()
        self.servicio = ServicioInventario(self.repositorio_productos, self.repositorio_movimientos)
        self.gestor_datos = GestorDatos()
        self.usuario_actual = "admin"
        
        # Cargar datos existentes o crear ejemplos
        if not self.gestor_datos.cargar_datos(self.servicio):
            self._cargar_datos_ejemplo()
    
    def _cargar_datos_ejemplo(self):
        """Cargar datos de ejemplo"""
        print("Cargando datos de ejemplo...")
        
        productos = [
            Producto("TECH001", "Laptop Dell XPS 15", "Laptop profesional Core i7 16GB", 1299.99, 5, "Tecnología"),
            Producto("TECH002", "Mouse Logitech MX Master", "Mouse inalámbrico ergonómico", 99.99, 20, "Tecnología"),
            Producto("TECH003", "Teclado Mecánico Corsair", "Teclado RGB switches Cherry MX", 149.99, 10, "Tecnología"),
            Producto("OFF001", "Silla Ergonómica", "Silla oficina premium", 899.99, 3, "Oficina"),
            Producto("OFF002", "Escritorio Ajustable", "Escritorio eléctrico sit-stand", 599.99, 5, "Oficina"),
            Producto("ACC001", "Monitor LG 27 4K", "Monitor UltraHD IPS", 449.99, 8, "Accesorios"),
            Producto("ACC002", "Webcam Logitech C920", "Webcam Full HD 1080p", 79.99, 15, "Accesorios"),
            Producto("NET001", "Router TP-Link AX6000", "Router WiFi 6 Gigabit", 299.99, 6, "Redes")
        ]
        
        for producto in productos:
            cantidad_inicial = random.randint(producto.stock_minimo, producto.stock_minimo * 3)
            self.servicio.registrar_producto(producto, cantidad_inicial, self.usuario_actual)
        
        # Generar movimientos de ventas
        self.servicio.retirar_stock("TECH002", 15, "Venta corporativa", self.usuario_actual)
        self.servicio.retirar_stock("TECH001", 2, "Venta cliente VIP", self.usuario_actual)
        self.servicio.retirar_stock("ACC002", 10, "Venta mayorista", self.usuario_actual)
        self.servicio.retirar_stock("TECH003", 8, "Venta online", self.usuario_actual)
        self.servicio.agregar_stock("TECH001", 3, "Reposición proveedor", self.usuario_actual)
        self.servicio.retirar_stock("ACC001", 4, "Venta local", self.usuario_actual)
        self.servicio.retirar_stock("NET001", 1, "Venta individual", self.usuario_actual)
        
        print("✓ Datos de ejemplo cargados correctamente")
    
    def limpiar_pantalla(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self, titulo):
        """Mostrar título"""
        print("\n" + "=" * 60)
        print(f"{titulo:^60}")
        print("=" * 60)
    
    def mostrar_menu(self, titulo, opciones):
        """Mostrar menú"""
        self.mostrar_titulo(titulo)
        for i, (opcion, _) in enumerate(opciones, 1):
            print(f"  {i}. {opcion}")
        print("=" * 60)
    
    def obtener_opcion(self, max_opcion):
        """Obtener opción del usuario"""
        while True:
            try:
                opcion = int(input(f"\nSeleccione opción (1-{max_opcion}): "))
                if 1 <= opcion <= max_opcion:
                    return opcion
                print(f"Opción inválida. Ingrese 1-{max_opcion}")
            except ValueError:
                print("Ingrese un número válido")
    
    def registrar_producto(self):
        """Registrar nuevo producto"""
        self.limpiar_pantalla()
        self.mostrar_titulo("REGISTRAR NUEVO PRODUCTO")
        
        try:
            print("\nIngrese datos del producto:")
            codigo = input("Código: ").strip().upper()
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            categoria = input("Categoría (General): ").strip() or "General"
            precio = float(input("Precio (S/): "))
            stock_minimo = int(input("Stock Mínimo: "))
            cantidad_inicial = int(input("Cantidad Inicial: "))
            codigo_barras = input("Código Barras (opcional): ").strip()
            
            producto = Producto(codigo, nombre, descripcion, precio, stock_minimo, categoria, codigo_barras)
            self.servicio.registrar_producto(producto, cantidad_inicial, self.usuario_actual)
            
            print(f"\n✓ Producto '{codigo}' registrado exitosamente!")
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def agregar_stock(self):
        """Agregar stock"""
        self.limpiar_pantalla()
        self.mostrar_titulo("AGREGAR STOCK")
        
        try:
            codigo = input("\nCódigo del producto: ").strip().upper()
            cantidad = int(input("Cantidad a agregar: "))
            descripcion = input("Descripción (opcional): ").strip()
            
            self.servicio.agregar_stock(codigo, cantidad, descripcion, self.usuario_actual)
            
            item = self.servicio.obtener_item_inventario(codigo)
            print(f"\n✓ Stock agregado exitosamente!")
            print(f"  Nuevo stock: {item.cantidad} unidades")
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def retirar_stock(self):
        """Retirar stock"""
        self.limpiar_pantalla()
        self.mostrar_titulo("RETIRAR STOCK")
        
        try:
            codigo = input("\nCódigo del producto: ").strip().upper()
            cantidad = int(input("Cantidad a retirar: "))
            descripcion = input("Descripción (opcional): ").strip()
            
            self.servicio.retirar_stock(codigo, cantidad, descripcion, self.usuario_actual)
            
            item = self.servicio.obtener_item_inventario(codigo)
            print(f"\n✓ Stock retirado exitosamente!")
            print(f"  Nuevo stock: {item.cantidad} unidades")
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def ver_inventario(self):
        """Ver inventario completo"""
        self.limpiar_pantalla()
        
        reporte = ReporteInventario()
        print(reporte.generar(self.servicio))
        
        input("\nPresione Enter para continuar...")
    
    def ver_movimientos(self):
        """Ver movimientos"""
        self.limpiar_pantalla()
        
        reporte = ReporteMovimientos()
        print(reporte.generar(self.servicio))
        
        input("\nPresione Enter para continuar...")
    
    def ver_alertas(self):
        """Ver alertas"""
        self.limpiar_pantalla()
        
        reporte = ReporteAlertas()
        print(reporte.generar(self.servicio))
        
        input("\nPresione Enter para continuar...")
    
    def ver_valorizacion(self):
        """Ver valorización"""
        self.limpiar_pantalla()
        
        reporte = ReporteValorizacion()
        print(reporte.generar(self.servicio))
        
        input("\nPresione Enter para continuar...")
    
    def ver_estadisticas(self):
        """Ver estadísticas"""
        self.limpiar_pantalla()
        self.mostrar_titulo("ESTADÍSTICAS DEL INVENTARIO")
        
        stats = self.servicio.get_estadisticas()
        
        print(f"\nTotal Productos: {stats['total_productos']}")
        print(f"Total Items: {stats['total_items']}")
        print(f"Valor Total: S/ {stats['valor_total']:,.2f}")
        print(f"Stock Bajo: {stats['stock_bajo_count']}")
        print(f"Stock Crítico: {stats['stock_critico_count']}")
        print(f"Categorías: {stats['categorias']}")
        
        # Productos más vendidos
        print("\nPRODUCTOS MÁS VENDIDOS:")
        print("-" * 50)
        mas_vendidos = self.servicio.obtener_productos_mas_vendidos(5)
        for i, (codigo, cantidad) in enumerate(mas_vendidos, 1):
            producto = self.repositorio_productos.obtener(codigo)
            if producto:
                print(f"{i}. {producto.nombre}: {cantidad} unidades")
        
        input("\nPresione Enter para continuar...")
    
    def buscar_producto(self):
        """Buscar producto"""
        self.limpiar_pantalla()
        self.mostrar_titulo("BUSCAR PRODUCTO")
        
        texto = input("\nIngrese código o nombre: ").strip()
        
        if not texto:
            print("No se ingresó texto de búsqueda")
            input("\nPresione Enter para continuar...")
            return
        
        resultados = self.repositorio_productos.buscar(texto)
        
        if resultados:
            print(f"\nSe encontraron {len(resultados)} productos:")
            print("-" * 80)
            print(f"{'Código':<10} {'Nombre':<30} {'Categoría':<15} {'Precio':<10} {'Stock':<10}")
            print("-" * 80)
            
            for producto in resultados:
                item = self.servicio.obtener_item_inventario(producto.codigo)
                stock = item.cantidad if item else 0
                print(f"{producto.codigo:<10} {producto.nombre:<30} {producto.categoria:<15} "
                      f"S/{producto.precio:<9.2f} {stock:<10}")
        else:
            print("\nNo se encontraron productos")
        
        input("\nPresione Enter para continuar...")
    
    def exportar_datos(self):
        """Exportar datos a CSV"""
        self.limpiar_pantalla()
        self.mostrar_titulo("EXPORTAR DATOS")
        
        print("\nSeleccione tipo de reporte:")
        print("1. Inventario completo")
        print("2. Movimientos")
        
        try:
            opcion = int(input("\nOpción: "))
            
            if opcion == 1:
                reporte = ReporteInventario()
                nombre_archivo = input("Nombre archivo CSV (sin extensión): ").strip()
                if not nombre_archivo:
                    nombre_archivo = f"inventario_{datetime.now().strftime('%Y%m%d')}"
                if not nombre_archivo.endswith('.csv'):
                    nombre_archivo += '.csv'
                
                reporte.exportar_csv(self.servicio, nombre_archivo)
                print(f"\n✓ Reporte exportado a: {nombre_archivo}")
                
            elif opcion == 2:
                reporte = ReporteMovimientos()
                nombre_archivo = input("Nombre archivo CSV (sin extensión): ").strip()
                if not nombre_archivo:
                    nombre_archivo = f"movimientos_{datetime.now().strftime('%Y%m%d')}"
                if not nombre_archivo.endswith('.csv'):
                    nombre_archivo += '.csv'
                
                reporte.exportar_csv(self.servicio, nombre_archivo)
                print(f"\n✓ Reporte exportado a: {nombre_archivo}")
            else:
                print("Opción inválida")
                
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def guardar_datos(self):
        """Guardar datos del sistema"""
        try:
            self.gestor_datos.guardar_datos(self.servicio)
            print("\n✓ Datos guardados exitosamente")
        except Exception as e:
            print(f"\n✗ Error al guardar: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def ejecutar(self):
        """Ejecutar sistema"""
        while True:
            self.limpiar_pantalla()
            
            menu_opciones = [
                ("Registrar nuevo producto", self.registrar_producto),
                ("Agregar stock", self.agregar_stock),
                ("Retirar stock", self.retirar_stock),
                ("Ver inventario completo", self.ver_inventario),
                ("Ver movimientos", self.ver_movimientos),
                ("Ver alertas de stock", self.ver_alertas),
                ("Ver valorización", self.ver_valorizacion),
                ("Ver estadísticas", self.ver_estadisticas),
                ("Buscar producto", self.buscar_producto),
                ("Exportar datos a CSV", self.exportar_datos),
                ("Guardar datos", self.guardar_datos),
                ("Salir", None)
            ]
            
            self.mostrar_menu("SISTEMA DE INVENTARIO - MENÚ PRINCIPAL", menu_opciones)
            opcion = self.obtener_opcion(len(menu_opciones))
            
            if opcion == len(menu_opciones):  # Salir
                print("\n¿Guardar datos antes de salir? (s/n): ", end="")
                if input().lower() == 's':
                    self.guardar_datos()
                print("\n¡Hasta luego!")
                break
            
            # Ejecutar opción seleccionada
            _, funcion = menu_opciones[opcion - 1]
            if funcion:
                funcion()


# ============= PROGRAMA PRINCIPAL =============

def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN DE INVENTARIOS - VERSIÓN CONSOLA")
    print("=" * 60)
    
    sistema = SistemaInventarioConsola()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
