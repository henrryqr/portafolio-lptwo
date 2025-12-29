import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Text
from datetime import datetime
import random
import string
import re
import sqlite3 # Para la base de datos
import shutil  # Para hacer backups
from tkcalendar import Calendar # Para el widget de calendario

# =================================================================================
# 🏦 SECCIÓN 1: GESTOR DE BASE DE DATOS (NUEVO)
# =================================================================================
class DatabaseManager:
    DB_NAME = "pagos.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()
        self.crear_tabla_transacciones()

    def crear_tabla_transacciones(self):
        """Crea la tabla si no existe."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_operacion TEXT NOT NULL UNIQUE,
            fecha TIMESTAMP NOT NULL,
            monto REAL NOT NULL,
            metodo TEXT NOT NULL,
            detalles TEXT,
            usuario TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'COMPLETED'
        )
        """)
        self.conn.commit()

    def insertar_pago(self, pago_obj, usuario):
        """Inserta un objeto de pago en la base de datos."""
        sql = """
        INSERT INTO transacciones (numero_operacion, fecha, monto, metodo, detalles, usuario, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            detalles = pago_obj.get_detalles_string()
            metodo = pago_obj.__class__.__name__ # Obtiene el nombre de la clase
            
            self.cursor.execute(sql, (
                pago_obj.numero_operacion,
                pago_obj.fecha,
                pago_obj.monto,
                metodo,
                detalles,
                usuario,
                'COMPLETED'
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar en BBDD: {e}")
            return False

    def get_pagos_por_fecha(self, fecha_str):
        """Busca pagos por fecha (formato YYYY-MM-DD)."""
        sql = """
        SELECT id, numero_operacion, fecha, monto, metodo, detalles, usuario, status
        FROM transacciones
        WHERE DATE(fecha) = ?
        ORDER BY fecha DESC
        """
        self.cursor.execute(sql, (fecha_str,))
        return self.cursor.fetchall()

    def cancelar_transaccion(self, num_operacion):
        """Actualiza el estado de una transacción a 'CANCELLED'."""
        sql = "UPDATE transacciones SET status = 'CANCELLED' WHERE numero_operacion = ?"
        self.cursor.execute(sql, (num_operacion,))
        self.conn.commit()
        return self.cursor.rowcount > 0 # Retorna True si se actualizó una fila

    def backup_database(self):
        """Crea una copia de seguridad de la base de datos."""
        try:
            backup_name = f"pagos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copyfile(self.DB_NAME, backup_name)
            return backup_name
        except Exception as e:
            print(f"Error en backup: {e}")
            return None

    def __del__(self):
        """Cierra la conexión al destruir el objeto."""
        self.conn.close()


# =================================================================================
# 💳 SECCIÓN 2: LÓGICA DE MÉTODOS DE PAGO (MODIFICADA)
# =================================================================================

class Pago:
    def __init__(self, monto):
        self.monto = monto
        self.fecha = datetime.now()
        self.numero_operacion = "OP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def realizar_pago(self):
        raise NotImplementedError("Subclases deben implementar este método")
        
    def get_detalles_string(self):
        """Retorna un string con detalles para la BBDD."""
        return "Sin detalles adicionales"

    def generar_voucher(self, metodo, detalles=""):
        voucher = f"""
        ========================================
                      VOUCHER DE PAGO
        ========================================
        Fecha: {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}
        Método de Pago: {metodo}
        Monto Original: S/.{self.monto:.2f}
        Número de Operación: {self.numero_operacion}
        {detalles}
        ========================================
         ¡Pago procesado exitosamente!
        ========================================
        """
        return "\n".join([line.strip() for line in voucher.split('\n')])

class TarjetaCredito(Pago):
    TASAS_INTERES = {1: 0.0, 3: 0.05, 6: 0.10, 12: 0.20, 32: 0.50}

    def __init__(self, monto, numero_tarjeta, nombre_titular, fecha_expiracion, cvv, cuotas=1):
        super().__init__(monto)
        self.numero_tarjeta = numero_tarjeta
        self.nombre_titular = nombre_titular
        self.cuotas = cuotas
        self.tasa_interes = self.TASAS_INTERES.get(cuotas, 0.0)
        self.monto_total_con_interes = self.monto * (1 + self.tasa_interes)
        self.monto_por_cuota = self.monto_total_con_interes / self.cuotas

    def realizar_pago(self):
        detalle_cuotas = f"en {self.cuotas} cuotas de S/.{self.monto_por_cuota:.2f} c/u (Total: S/.{self.monto_total_con_interes:.2f})" if self.cuotas > 1 else "en 1 cuota."
        return f"💳 Pago con tarjeta N° ...{self.numero_tarjeta[-4:]} procesado {detalle_cuotas}"
        
    def get_detalles_string(self):
        return f"Titular: {self.nombre_titular}, Tarjeta: ...{self.numero_tarjeta[-4:]}, Cuotas: {self.cuotas}"

    def generar_voucher(self):
        detalles = f"Titular: {self.nombre_titular}\nTarjeta: **** **** **** {self.numero_tarjeta[-4:]}"
        if self.cuotas > 1:
            detalles += (f"\n----------------------------------------\n"
                         f"Detalle de Cuotas: {self.cuotas} (Total: S/.{self.monto_total_con_interes:.2f})")
        return super().generar_voucher("Tarjeta de Crédito", detalles)

class Efectivo(Pago):
    def __init__(self, monto, nombre, dni):
        super().__init__(monto)
        self.nombre = nombre
        self.dni = dni
    def realizar_pago(self):
        return f"💵 Pago en efectivo recibido de {self.nombre} (DNI: {self.dni})."
    def get_detalles_string(self):
        return f"Cliente: {self.nombre}, DNI: {self.dni}"
    def generar_voucher(self):
        detalles = f"Nombre Cliente: {self.nombre}\nDNI Cliente: {self.dni}"
        return super().generar_voucher("Efectivo", detalles)

class PayPal(Pago):
    def __init__(self, monto, correo, nombre_remitente, cuenta_origen):
        super().__init__(monto)
        self.correo = correo
        self.nombre_remitente = nombre_remitente
    def realizar_pago(self):
        return f"🌐 Pago con PayPal ({self.correo}) por S/.{self.monto:.2f} realizado."
    def get_detalles_string(self):
        return f"Correo: {self.correo}, Remitente: {self.nombre_remitente}"
    def generar_voucher(self):
        detalles = f"Correo: {self.correo}\nRemitente: {self.nombre_remitente}"
        return super().generar_voucher("PayPal", detalles)

class Yape(Pago):
    def __init__(self, monto, numero, nombre_remitente, cuenta_origen):
        super().__init__(monto)
        self.numero = numero
        self.nombre_remitente = nombre_remitente
    def realizar_pago(self):
        return f"📱 Pago con Yape al {self.numero} por S/.{self.monto:.2f} realizado."
    def get_detalles_string(self):
        return f"Número: {self.numero}, Remitente: {self.nombre_remitente}"
    def generar_voucher(self):
        detalles = f"Número: {self.numero}\nRemitente: {self.nombre_remitente}"
        return super().generar_voucher("Yape", detalles)

class Plin(Pago):
    def __init__(self, monto, numero, nombre_remitente, cuenta_origen):
        super().__init__(monto)
        self.numero = numero
        self.nombre_remitente = nombre_remitente
    def realizar_pago(self):
        return f"📲 Pago con Plin al {self.numero} por S/.{self.monto:.2f} realizado."
    def get_detalles_string(self):
        return f"Número: {self.numero}, Remitente: {self.nombre_remitente}"
    def generar_voucher(self):
        detalles = f"Número: {self.numero}\nRemitente: {self.nombre_remitente}"
        return super().generar_voucher("Plin", detalles)

class TransferenciaBancaria(Pago):
    def __init__(self, monto, usuario, password, cuenta_destino_num, banco):
        super().__init__(monto)
        self.usuario = usuario
        self.password = password
        self.cuenta_destino_num = cuenta_destino_num
        self.banco = banco
    def realizar_pago(self):
        cuenta_origen = self.banco.autenticar(self.usuario, self.password)
        if not cuenta_origen: raise ValueError("Usuario o contraseña incorrectos.")
        if self.cuenta_destino_num not in self.banco.cuentas: raise ValueError("Cuenta destino no existe.")
        if self.cuenta_destino_num == cuenta_origen.numero_cuenta: raise ValueError("No puede transferir a su propia cuenta.")
        cuenta_destino = self.banco.cuentas[self.cuenta_destino_num]
        txn = Transferencia(self.monto, cuenta_origen, cuenta_destino)
        resultado = txn.procesar()
        self.numero_operacion = txn.numero_operacion # Sobrescribir el N° op
        return f"💸 {resultado}"
    def get_detalles_string(self):
        return f"Usuario Origen: {self.usuario}, Cta Destino: {self.cuenta_destino_num}"
    def generar_voucher(self):
        detalles = f"Usuario Origen: {self.usuario}\nCuenta Destino: {self.cuenta_destino_num}"
        return super().generar_voucher("Transferencia Bancaria", detalles)

# =================================================================================
# 🔑 SECCIÓN 3: AUTENTICACIÓN Y LOGIN
# =================================================================================

# --- Paleta de Colores Corporativa ---
COLOR_BG = "#f0f4f8"
COLOR_FRAME_BG = "#ffffff"
COLOR_HEADER = "#003366"
COLOR_BUTTON = "#0056b3"
COLOR_BUTTON_FG = "#ffffff"
COLOR_BUTTON_HOVER = "#004494"
COLOR_LABEL = "#212529"
COLOR_ERROR_BG = "#fdedec"

class SistemaAutenticacion:
    def __init__(self):
        self.usuarios = { "henrryqr": "75327974" } # Usuario único
    
    def validar_credenciales(self, usuario, contraseña):
        return self.usuarios.get(usuario) == contraseña

class VentanaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.auth_system = SistemaAutenticacion()
        self.title("Acceso Seguro - Banco Digital")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)
        
        self.parent.update_idletasks()
        parent_width = self.parent.winfo_screenwidth()
        parent_height = self.parent.winfo_screenheight()
        x = (parent_width // 2) - (400 // 2)
        y = (parent_height // 2) - (300 // 2)
        self.geometry(f'+{x}+{y}')

        self.transient(parent)
        self.grab_set()
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_LABEL, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=COLOR_BG, foreground=COLOR_HEADER, font=("Segoe UI", 18, "bold"))
        style.configure("TButton", background=COLOR_BUTTON, foreground=COLOR_BUTTON_FG, font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[('active', COLOR_BUTTON_HOVER)])
        
        frame = ttk.Frame(self, padding=30, style="TFrame")
        frame.pack(expand=True, fill="both")
        style.configure("TFrame", background=COLOR_BG)

        ttk.Label(frame, text="Banco Digital", style="Header.TLabel").pack(pady=(0, 25))
        
        ttk.Label(frame, text="Usuario:").pack(pady=(5,0), anchor="w")
        self.user_entry = ttk.Entry(frame, width=40, font=("Segoe UI", 10))
        self.user_entry.pack(pady=(0, 15), fill="x")
        
        ttk.Label(frame, text="Contraseña:").pack(pady=(5,0), anchor="w")
        self.pass_entry = ttk.Entry(frame, width=40, show="*", font=("Segoe UI", 10))
        self.pass_entry.pack(pady=(0, 15), fill="x")
        
        self.login_button = ttk.Button(frame, text="Ingresar", command=self._intentar_login, style="TButton")
        self.login_button.pack(pady=10, fill="x")
        
        self.error_label = ttk.Label(frame, text="", foreground="#c0392b", style="TLabel")
        self.error_label.pack()

        self.pass_entry.bind("<Return>", self._intentar_login)
        self.user_entry.bind("<Return>", lambda e: self.pass_entry.focus())
        self.user_entry.focus_set()
        
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)

    def _intentar_login(self, event=None):
        usuario = self.user_entry.get()
        password = self.pass_entry.get()
        
        if self.auth_system.validar_credenciales(usuario, password):
            self.destroy()
            self.parent.deiconify()
            VentanaPagos(self.parent, usuario, DatabaseManager()) # Pasa el usuario y el gestor de BBDD
        else:
            self.error_label.config(text="Usuario o contraseña incorrectos")
            self.pass_entry.delete(0, tk.END)

# =================================================================================
# 🗓️ SECCIÓN 4: VENTANA DE HISTORIAL (NUEVA)
# =================================================================================
class VentanaHistorial(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db = db_manager
        self.title("Gestor de Transacciones y Backup")
        self.geometry("900x600")
        self.configure(bg=COLOR_BG)
        self.transient(parent)
        self.grab_set()
        
        # Frame superior para controles
        control_frame = ttk.Frame(self, padding=10, style="Main.TFrame")
        control_frame.pack(fill="x")
        
        # --- Calendario ---
        cal_frame = ttk.LabelFrame(control_frame, text="Seleccionar Fecha", padding=10)
        cal_frame.pack(side="left", padx=10, pady=10, fill="y")
        self.calendar = Calendar(cal_frame, selectmode='day', date_pattern='y-mm-dd')
        self.calendar.pack()
        
        ttk.Button(cal_frame, text="Buscar Transacciones", command=self.buscar_historial).pack(pady=10, fill="x")

        # --- Acciones ---
        action_frame = ttk.LabelFrame(control_frame, text="Acciones", padding=10)
        action_frame.pack(side="left", padx=10, pady=10, fill="y")
        
        ttk.Button(action_frame, text="🚫 Cancelar Transacción Seleccionada", command=self.cancelar_seleccionado).pack(pady=5, fill="x")
        ttk.Separator(action_frame, orient='horizontal').pack(pady=10, fill='x')
        ttk.Button(action_frame, text="💾 Crear Backup de Base de Datos", command=self.realizar_backup).pack(pady=5, fill="x")

        # --- Treeview para resultados ---
        tree_frame = ttk.Frame(self, padding=10, style="Main.TFrame")
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("ID", "N° Operación", "Fecha y Hora", "Monto", "Método", "Estado", "Usuario", "Detalles")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
        
        # Ajustar anchos de columna
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("N° Operación", width=120)
        self.tree.column("Fecha y Hora", width=140)
        self.tree.column("Monto", width=80, anchor="e")
        self.tree.column("Método", width=100)
        self.tree.column("Estado", width=90, anchor="center")
        self.tree.column("Usuario", width=80)
        self.tree.column("Detalles", width=200)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(fill="both", expand=True)

        # --- Estilos para Treeview (Colorear filas) ---
        self.tree.tag_configure('COMPLETED', background='#d4edda') # Verde
        self.tree.tag_configure('CANCELLED', background='#f8d7da', foreground='#721c24') # Rojo
        
        self.buscar_historial() # Cargar el día actual al abrir

    def buscar_historial(self):
        """Obtiene la fecha del calendario y la consulta en la BBDD."""
        fecha_sel = self.calendar.get_date()
        
        # Limpiar treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Consultar BBDD
        registros = self.db.get_pagos_por_fecha(fecha_sel)
        
        if not registros:
            messagebox.showinfo("Sin Resultados", f"No se encontraron transacciones para el {fecha_sel}", parent=self)
            return
            
        # Llenar treeview
        for reg in registros:
            # (id, num_op, fecha, monto, metodo, detalles, usuario, status)
            monto_str = f"S/.{reg[3]:.2f}"
            fecha_str = datetime.strptime(reg[2], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
            status = reg[7]
            self.tree.insert("", "end", values=(reg[0], reg[1], fecha_str, monto_str, reg[4], status, reg[6], reg[5]), tags=(status,))

    def cancelar_seleccionado(self):
        """Cancela la transacción seleccionada en el Treeview."""
        try:
            item_sel = self.tree.focus()
            if not item_sel:
                raise ValueError("Por favor, seleccione una transacción de la lista.")
            
            valores = self.tree.item(item_sel, "values")
            num_operacion = valores[1]
            status_actual = valores[5]

            if status_actual == 'CANCELLED':
                raise ValueError("Esta transacción ya ha sido cancelada.")

            if not messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de que desea cancelar la transacción {num_operacion}?\n\nEsta acción no se puede deshacer.", parent=self):
                return
            
            # Actualizar BBDD
            if self.db.cancelar_transaccion(num_operacion):
                messagebox.showinfo("Éxito", f"Transacción {num_operacion} ha sido cancelada.", parent=self)
                # Refrescar la vista
                self.buscar_historial()
            else:
                raise Exception("No se pudo actualizar la base de datos.")

        except (ValueError, Exception) as e:
            messagebox.showerror("Error", str(e), parent=self)

    def realizar_backup(self):
        """Inicia el proceso de backup."""
        if not messagebox.askyesno("Confirmar Backup", "¿Desea crear una copia de seguridad de la base de datos ahora?", parent=self):
            return
            
        backup_file = self.db.backup_database()
        if backup_file:
            messagebox.showinfo("Backup Exitoso", f"Copia de seguridad creada con éxito:\n{backup_file}", parent=self)
        else:
            messagebox.showerror("Error de Backup", "No se pudo crear la copia de seguridad.", parent=self)


# =================================================================================
# 🖥️ SECCIÓN 5: VENTANA PRINCIPAL DE PAGOS (MODIFICADA)
# =================================================================================
class VentanaPagos:
    def __init__(self, root, usuario, db_manager):
        self.root = root
        self.usuario = usuario
        self.db = db_manager # Gestor de BBDD
        self.banco = self._setup_banco_demo()
        self.campos_widgets = {}
        
        self._configurar_ventana()
        self._crear_widgets()

    def _setup_banco_demo(self):
        banco = Banco()
        c1 = banco.crear_cuenta("Usuario Origen", 1500)
        c2 = banco.crear_cuenta("Tienda Destino", 500)
        banco.registrar_usuario("user1", "pass123", c1)
        return banco

    def _configurar_ventana(self):
        self.root.title(f"Terminal de Pagos - (Usuario: {self.usuario})")
        self.root.geometry("600x750") # Un poco más alto
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)
        
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (750 // 2)
        self.root.geometry(f'+{x}+{y}')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background=COLOR_FRAME_BG, foreground=COLOR_LABEL, font=("Segoe UI", 10))
        style.configure("TButton", background=COLOR_BUTTON, foreground=COLOR_BUTTON_FG, font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[('active', COLOR_BUTTON_HOVER), ('disabled', '#c0c0c0')])
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("Main.TFrame", background=COLOR_BG)
        style.configure("Content.TFrame", background=COLOR_FRAME_BG)
        style.configure("TLabelFrame", background=COLOR_FRAME_BG, borderwidth=1, relief="solid")
        style.configure("TLabelFrame.Label", background=COLOR_FRAME_BG, foreground=COLOR_HEADER, font=("Segoe UI", 11, "bold"))
        style.configure("Header.TLabel", background=COLOR_BG, foreground=COLOR_HEADER, font=("Segoe UI", 18, "bold"))
        style.configure("Info.TLabel", background=COLOR_FRAME_BG, foreground="#5d6d7e", font=("Segoe UI", 9, "italic"))
        style.configure("Error.TEntry", fieldbackground=COLOR_ERROR_BG, bordercolor="red", foreground="black")

    def _crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20, style="Main.TFrame")
        main_frame.pack(expand=True, fill="both")

        # --- BOTÓN DE GESTIÓN ---
        gestion_frame = ttk.Frame(main_frame, style="Main.TFrame")
        gestion_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(gestion_frame, text="Terminal de Pagos", style="Header.TLabel").pack(side="left")
        ttk.Button(gestion_frame, text="📊 Gestor de Transacciones", command=self.abrir_gestor).pack(side="right")
        # --- FIN BOTÓN GESTIÓN ---

        datos_pago_frame = ttk.LabelFrame(main_frame, text=" 1. Información de la Transacción ", padding=20)
        datos_pago_frame.pack(fill="x", pady=10)
        
        ttk.Label(datos_pago_frame, text="Monto a Pagar (S/.):").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.monto_entry = ttk.Entry(datos_pago_frame, width=30)
        self.monto_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=8)
        
        ttk.Label(datos_pago_frame, text="Método de Pago:").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        metodos = ["Tarjeta de Crédito", "Efectivo", "PayPal", "Yape", "Plin", "Transferencia Bancaria"]
        self.metodo_combo = ttk.Combobox(datos_pago_frame, values=metodos, state="readonly", width=28)
        self.metodo_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=8)
        self.metodo_combo.current(0)
        self.metodo_combo.bind("<<ComboboxSelected>>", self._actualizar_campos_dinamicos)
        datos_pago_frame.columnconfigure(1, weight=1)

        self.frame_adicional = ttk.LabelFrame(main_frame, text=" 2. Datos del Método de Pago ", padding=20)
        self.frame_adicional.pack(fill="x", pady=10)
        self.frame_adicional.columnconfigure(1, weight=1)

        accion_frame = ttk.LabelFrame(main_frame, text=" 3. Confirmación ", padding=20)
        accion_frame.pack(fill="x", pady=10)
        
        self.cuotas_info_label = ttk.Label(accion_frame, text="", style="Info.TLabel")
        self.cuotas_info_label.pack(pady=5, fill="x")
        
        self.boton_procesar = ttk.Button(accion_frame, text="Procesar Pago", command=self.procesar_pago, state="disabled")
        self.boton_procesar.pack(fill="x", pady=10)
        
        self.resultado_label = ttk.Label(main_frame, text="", wraplength=500, anchor="center", style="Main.TLabel")
        self.resultado_label.pack(pady=10)

        self.monto_entry.bind("<KeyRelease>", self._validar_formulario)
        self._actualizar_campos_dinamicos()
        
    def abrir_gestor(self):
        """Abre la nueva ventana de historial."""
        VentanaHistorial(self.root, self.db)

    def _agregar_campo(self, label_text, key, grid_row, is_password=False):
        ttk.Label(self.frame_adicional, text=label_text).grid(row=grid_row, column=0, sticky="w", padx=5, pady=8)
        entry = ttk.Entry(self.frame_adicional, width=30, show="*" if is_password else "")
        entry.grid(row=grid_row, column=1, sticky="ew", padx=5, pady=8)
        entry.bind("<KeyRelease>", self._validar_formulario)
        self.campos_widgets[key] = entry
        
    def _actualizar_campos_dinamicos(self, event=None):
        for widget in self.frame_adicional.winfo_children():
            widget.destroy()
        self.campos_widgets.clear()
        self.cuotas_info_label.config(text="")
        
        metodo = self.metodo_combo.get()
        if metodo == "Tarjeta de Crédito":
            self._agregar_campo("Número de Tarjeta (16):", "numero_tarjeta", 0)
            self._agregar_campo("Nombre del Titular:", "nombre_titular", 1)
            self._agregar_campo("Expiración (MM/AA):", "fecha_expiracion", 2)
            self._agregar_campo("CVV (3-4):", "cvv", 3)
            ttk.Label(self.frame_adicional, text="Cuotas:").grid(row=4, column=0, sticky="w", padx=5, pady=8)
            cuotas_options = ["1 (Sin interés)", "3 cuotas (5%)", "6 cuotas (10%)", "12 cuotas (20%)", "32 cuotas (50%)"]
            combo_cuotas = ttk.Combobox(self.frame_adicional, values=cuotas_options, state="readonly", width=28)
            combo_cuotas.grid(row=4, column=1, sticky="ew", padx=5, pady=8)
            combo_cuotas.current(0)
            combo_cuotas.bind("<<ComboboxSelected>>", self._actualizar_info_cuotas)
            self.campos_widgets["cuotas"] = combo_cuotas

        elif metodo == "Efectivo":
            self._agregar_campo("Nombre Completo:", "nombre", 0)
            self._agregar_campo("DNI (8 dígitos):", "dni", 1)
        
        elif metodo == "PayPal":
            self._agregar_campo("Correo Electrónico:", "correo", 0)
            self._agregar_campo("Nombre del Remitente:", "nombre_remitente", 1)
            self._agregar_campo("Cuenta Origen:", "cuenta_origen", 2) # Simulación
        elif metodo in ["Yape", "Plin"]:
            self._agregar_campo("Número de Teléfono (9):", "numero", 0)
            self._agregar_campo("Nombre Remitente:", "nombre_remitente", 1)
            self._agregar_campo("Cuenta Origen:", "cuenta_origen", 2) # Simulación
        elif metodo == "Transferencia Bancaria":
            self._agregar_campo("Usuario Bancario:", "usuario", 0)
            self._agregar_campo("Contraseña:", "password", 1, is_password=True)
            self._agregar_campo("Cuenta Destino (10):", "cuenta_destino", 2)
        
        self._validar_formulario()

    def _actualizar_info_cuotas(self, event=None):
        try:
            monto = float(self.monto_entry.get())
            cuotas_str = self.campos_widgets["cuotas"].get()
            cuotas = int(re.match(r"(\d+)", cuotas_str).group(1))
            
            if cuotas > 1:
                tasa = TarjetaCredito.TASAS_INTERES[cuotas]
                total = monto * (1 + tasa)
                monto_cuota = total / cuotas
                self.cuotas_info_label.config(text=f"Total: S/.{total:.2f}  |  {cuotas} cuotas de S/.{monto_cuota:.2f} c/u")
            else:
                self.cuotas_info_label.config(text="Pago en 1 cuota (sin interés).")
        except (ValueError, KeyError, TypeError):
            self.cuotas_info_label.config(text="Ingrese un monto válido para calcular las cuotas.")

    def _validar_formulario(self, event=None):
        es_valido = True
        
        monto_str = self.monto_entry.get()
        try:
            if not (monto_str and float(monto_str) > 0):
                es_valido = False
        except ValueError:
            es_valido = False
        
        for key, widget in self.campos_widgets.items():
            if isinstance(widget, ttk.Entry) and not widget.get().strip():
                es_valido = False
        
        self.boton_procesar.config(state="normal" if es_valido else "disabled")
        self._resaltar_errores(validando=True)
        
    def _resaltar_errores(self, validando=False):
        # (Lógica de resaltado sin cambios)
        for key, widget in self.campos_widgets.items():
            if not isinstance(widget, ttk.Entry): continue
            valido = True
            valor = widget.get().strip()
            if valor or validando:
                if key == "numero_tarjeta" and not re.match(r"^\d{16}$", valor): valido = False
                elif key == "fecha_expiracion" and not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", valor): valido = False
                elif key == "cvv" and not re.match(r"^\d{3,4}$", valor): valido = False
                elif key == "dni" and not re.match(r"^\d{8}$", valor): valido = False
                elif key == "numero" and not re.match(r"^\d{9}$", valor): valido = False
                elif key == "correo" and not re.match(r"[^@]+@[^@]+\.[^@]+", valor): valido = False
                elif key == "cuenta_destino" and not re.match(r"^\d{10}$", valor): valido = False
            if not valor and not validando: valido = True
            widget.config(style="TEntry" if valido else "Error.TEntry")
            
    def procesar_pago(self):
        self._resaltar_errores(validando=True)
        
        try:
            monto = float(self.monto_entry.get())
            metodo = self.metodo_combo.get()
            datos = {k: w.get().strip() for k, w in self.campos_widgets.items()}
            
            pago_obj = None
            if metodo == "Tarjeta de Crédito":
                cuotas = int(re.match(r"(\d+)", datos["cuotas"]).group(1))
                pago_obj = TarjetaCredito(monto, datos["numero_tarjeta"], datos["nombre_titular"], datos["fecha_expiracion"], datos["cvv"], cuotas)
            elif metodo == "Efectivo":
                pago_obj = Efectivo(monto, datos["nombre"], datos["dni"])
            elif metodo == "PayPal":
                pago_obj = PayPal(monto, datos["correo"], datos["nombre_remitente"], datos.get("cuenta_origen", ""))
            elif metodo == "Yape":
                pago_obj = Yape(monto, datos["numero"], datos["nombre_remitente"], datos.get("cuenta_origen", ""))
            elif metodo == "Plin":
                pago_obj = Plin(monto, datos["numero"], datos["nombre_remitente"], datos.get("cuenta_origen", ""))
            elif metodo == "Transferencia Bancaria":
                pago_obj = TransferenciaBancaria(monto, datos["usuario"], datos["password"], datos["cuenta_destino"], self.banco)
            
            # 1. Realizar la simulación del pago
            resultado = pago_obj.realizar_pago()
            
            # 2. Si el pago es exitoso, INSERTAR EN BBDD
            if not self.db.insertar_pago(pago_obj, self.usuario):
                raise Exception("Error al guardar la transacción en la base de datos.")

            # 3. Mostrar éxito y voucher
            self.resultado_label.config(text=f"✅ ¡Éxito! {resultado}", foreground="#1e8449")
            voucher = pago_obj.generar_voucher()
            self._mostrar_voucher(voucher)
            self._limpiar_campos()

        except (ValueError, KeyError, AttributeError, TypeError) as e:
            self.resultado_label.config(text=f"❌ Error: {e}", foreground="#c0392b")
            messagebox.showerror("Error de Validación", f"No se pudo procesar el pago:\n\n{e}\n\nPor favor, revise todos los campos.")
    
    def _limpiar_campos(self):
        self.monto_entry.delete(0, tk.END)
        for widget in self.campos_widgets.values():
            if isinstance(widget, ttk.Combobox):
                widget.current(0)
            else:
                widget.config(style="TEntry")
                widget.delete(0, tk.END)
        self.resultado_label.config(text="")
        self.cuotas_info_label.config(text="")
        self._validar_formulario()
        
    def _mostrar_voucher(self, voucher_texto):
        VoucherWindow(self.root, voucher_texto)

# =================================================================================
# 📄 SECCIÓN 6: VENTANA DE VOUCHER (Sin cambios)
# =================================================================================
class VoucherWindow(tk.Toplevel):
    def __init__(self, parent, voucher_texto):
        super().__init__(parent)
        self.title("Voucher de Pago")
        self.geometry("400x500")
        self.configure(bg=COLOR_FRAME_BG)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        x = parent_x + (parent_width // 2) - (400 // 2)
        y = parent_y + (parent_height // 2) - (500 // 2)
        self.geometry(f'+{x}+{y}')

        style = ttk.Style()
        style.configure("Voucher.TLabel", background=COLOR_FRAME_BG, foreground=COLOR_HEADER, font=("Segoe UI", 16, "bold"))
        style.configure("Voucher.TFrame", background=COLOR_FRAME_BG)
        
        ttk.Label(self, text="Voucher Generado", style="Voucher.TLabel").pack(pady=15)
        
        text_widget = Text(self, height=20, width=50, font=("Courier", 10), wrap="word", bg="#f4f6f7", bd=1, relief="solid")
        text_widget.insert(tk.END, voucher_texto)
        text_widget.config(state="disabled")
        text_widget.pack(pady=5, padx=20, fill="both", expand=True)
        
        botones_frame = ttk.Frame(self, style="Voucher.TFrame", padding=(0, 0, 0, 10))
        botones_frame.pack(pady=15)

        ttk.Button(botones_frame, text="Guardar como TXT", command=lambda: self._guardar(voucher_texto)).pack(side="left", padx=10)
        ttk.Button(botones_frame, text="Cerrar", command=self.destroy).pack(side="left", padx=10)
        
    def _guardar(self, texto):
        op_match = re.search(r"(OP-|TXN-)[A-Z0-9]+", texto)
        default_name = op_match.group(0) if op_match else "voucher"
        
        filepath = filedialog.asksaveasfilename(
            initialfile=f"{default_name}.txt",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(texto)
            messagebox.showinfo("Guardado", "Voucher guardado exitosamente.", parent=self)
            self.destroy()

# =================================================================================
# 🚀 SECCIÓN 7: PUNTO DE ENTRADA DE LA APLICACIÓN
# =================================================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # Inicia el login. El login se encargará de crear el DatabaseManager
    # y pasarlo a la VentanaPagos al tener éxito.
    login_app = VentanaLogin(root)
    
    root.mainloop()
