import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Text
from datetime import datetime
import random
import string
import re

# -----------------------------------
# CLASE BASE (MEJORADA CON VOUCHER)
# -----------------------------------
class Pago:
    def __init__(self, monto):
        self.monto = monto
        self.fecha = datetime.now()
        self.numero_operacion = self.generar_numero_operacion()

    def generar_numero_operacion(self):
        """Genera un número de operación único."""
        return "OP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def realizar_pago(self):
        return f"Procesando pago de S/.{self.monto:.2f}"

    def generar_voucher(self, metodo_pago, detalles_especificos):
        """Genera el texto base del voucher."""
        voucher_texto = f"""
        ========================================
                 VOUCHER DE PAGO
        ========================================
        Fecha: {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}
        Número de Operación: {self.numero_operacion}
        Monto: S/.{self.monto:.2f}
        Método de Pago: {metodo_pago}
        ----------------------------------------
        DETALLES DE LA OPERACIÓN:
        {detalles_especificos}
        ========================================
           ¡Gracias por su preferencia!
        ========================================
        """
        # Limpiar la indentación del texto
        return "\n".join([line.strip() for line in voucher_texto.split('\n')])


# -----------------------------------
# SUBCLASES (ACTUALIZADAS)
# -----------------------------------
class TarjetaCredito(Pago):
    def __init__(self, monto, numero_tarjeta, titular, expiracion, cvv):
        super().__init__(monto)
        self.numero_tarjeta = numero_tarjeta
        self.titular = titular
        self.expiracion = expiracion
        self.cvv = cvv # El CVV no debería almacenarse post-transacción, pero se usa para el pago

    def realizar_pago(self):
        return f"💳 Pago de S/.{self.monto:.2f} con tarjeta N° ...{self.numero_tarjeta[-4:]} (Titular: {self.titular}) realizado correctamente."

    def generar_voucher(self):
        detalles = (
            f"Titular: {self.titular}\n"
            f"Tarjeta: **** **** **** {self.numero_tarjeta[-4:]}\n"
            f"Expiración: {self.expiracion}"
        )
        return super().generar_voucher("Tarjeta de Crédito", detalles)


class PayPal(Pago):
    def __init__(self, monto, correo, nombre_remitente):
        super().__init__(monto)
        self.correo = correo
        self.nombre_remitente = nombre_remitente

    def realizar_pago(self):
        return f"🌐 Pago de S/.{self.monto:.2f} mediante PayPal ({self.correo}) realizado correctamente."

    def generar_voucher(self):
        detalles = (
            f"Correo PayPal: {self.correo}\n"
            f"Remitente: {self.nombre_remitente}"
        )
        return super().generar_voucher("PayPal", detalles)


class Efectivo(Pago):
    def __init__(self, monto, nombre_cliente, dni_cliente):
        super().__init__(monto)
        self.nombre_cliente = nombre_cliente
        self.dni_cliente = dni_cliente

    def realizar_pago(self):
        return f"💵 Pago en efectivo de S/.{self.monto:.2f} recibido (Cliente: {self.nombre_cliente})."

    def generar_voucher(self):
        detalles = (
            f"Cliente: {self.nombre_cliente}\n"
            f"DNI: {self.dni_cliente}"
        )
        return super().generar_voucher("Efectivo", detalles)


class Yape(Pago):
    def __init__(self, monto, numero, nombre_remitente):
        super().__init__(monto)
        self.numero = numero
        self.nombre_remitente = nombre_remitente

    def realizar_pago(self):
        return f"📱 Pago de S/.{self.monto:.2f} realizado con Yape desde {self.nombre_remitente}."

    def generar_voucher(self):
        detalles = (
            f"Número: {self.numero}\n"
            f"Remitente: {self.nombre_remitente}"
        )
        return super().generar_voucher("Yape", detalles)


class Plin(Pago):
    def __init__(self, monto, numero, nombre_remitente):
        super().__init__(monto)
        self.numero = numero
        self.nombre_remitente = nombre_remitente

    def realizar_pago(self):
        return f"📲 Pago de S/.{self.monto:.2f} realizado con Plin desde {self.nombre_remitente}."

    def generar_voucher(self):
        detalles = (
            f"Número: {self.numero}\n"
            f"Remitente: {self.nombre_remitente}"
        )
        return super().generar_voucher("Plin", detalles)


# -----------------------------------
# SISTEMA DE AUTENTICACIÓN (Sin cambios)
# -----------------------------------
class SistemaAutenticacion:
    def __init__(self):
        self.usuarios = {
            "admin": "admin123",
            "usuario": "usuario123",
            "cajero": "cajero123"
        }
    
    def validar_credenciales(self, usuario, contraseña):
        return self.usuarios.get(usuario) == contraseña


# -----------------------------------
# VENTANA DE LOGIN (Sin cambios)
# -----------------------------------
class VentanaLogin:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_system = SistemaAutenticacion()
        
        self.root.title("🔐 Inicio de Sesión - Sistema de Pagos")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(pady=(0, 20))
        
        tk.Label(header_frame, text="💳", font=("Arial", 60), bg="#1a1a2e").pack()
        
        tk.Label(
            main_frame, 
            text="SISTEMA DE PAGOS", 
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        ).pack(pady=(0, 5))
        
        tk.Label(
            main_frame, 
            text="Inicia sesión para continuar", 
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg="#a0a0a0"
        ).pack(pady=(0, 30))
        
        form_frame = tk.Frame(main_frame, bg="#16213e", relief="flat")
        form_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            form_frame, 
            text="Usuario", 
            font=("Segoe UI", 11, "bold"),
            bg="#16213e",
            fg="#ffffff",
            anchor="w"
        ).pack(pady=(20, 5), padx=20, fill="x")
        
        self.usuario_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#0f3460",
            fg="#ffffff",
            relief="flat",
            insertbackground="#00d4ff"
        )
        self.usuario_entry.pack(pady=(0, 15), padx=20, fill="x", ipady=8)
        
        tk.Label(
            form_frame, 
            text="Contraseña", 
            font=("Segoe UI", 11, "bold"),
            bg="#16213e",
            fg="#ffffff",
            anchor="w"
        ).pack(pady=(0, 5), padx=20, fill="x")
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#0f3460",
            fg="#ffffff",
            show="●",
            relief="flat",
            insertbackground="#00d4ff"
        )
        self.password_entry.pack(pady=(0, 20), padx=20, fill="x", ipady=8)
        
        self.login_btn = tk.Button(
            main_frame,
            text="INICIAR SESIÓN",
            font=("Segoe UI", 12, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            relief="flat",
            cursor="hand2",
            command=self.intentar_login,
            activebackground="#00b8d4",
            activeforeground="#1a1a2e"
        )
        self.login_btn.pack(pady=20, padx=20, fill="x", ipady=10)
        
        info_frame = tk.Frame(main_frame, bg="#16213e", relief="flat")
        info_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(
            info_frame, 
            text="👤 Usuarios de prueba:", 
            font=("Segoe UI", 9, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        ).pack(pady=(10, 5))
        
        usuarios_info = [
            "admin / admin123",
            "usuario / usuario123",
            "cajero / cajero123"
        ]
        
        for info in usuarios_info:
            tk.Label(
                info_frame, 
                text=info, 
                font=("Consolas", 9),
                bg="#16213e",
                fg="#a0a0a0"
            ).pack()
        
        tk.Label(info_frame, text="", bg="#16213e").pack(pady=5)
        
        self.password_entry.bind("<Return>", lambda e: self.intentar_login())
        
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 9),
            bg="#1a1a2e",
            fg="#ff6b6b"
        )
        self.status_label.pack()
        
    def intentar_login(self):
        usuario = self.usuario_entry.get().strip()
        contraseña = self.password_entry.get().strip()
        
        if not usuario or not contraseña:
            self.status_label.config(text="❌ Por favor complete todos los campos")
            return
        
        if self.auth_system.validar_credenciales(usuario, contraseña):
            self.status_label.config(text="✓ Acceso concedido...", fg="#51cf66")
            self.root.after(500, lambda: self.on_login_success(usuario))
        else:
            self.status_label.config(text="❌ Usuario o contraseña incorrectos", fg="#ff6b6b")
            self.password_entry.delete(0, tk.END)


# -----------------------------------
# INTERFAZ DE PAGOS (ACTUALIZADA)
# -----------------------------------
class VentanaPagos:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("💰 Sistema de Pagos")
        self.root.geometry("500x800") # --- Más alta para nuevos campos
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")
        
        # --- Diccionario para guardar los campos de entrada dinámicos
        self.campos_adicionales = {}
        
        # Header
        header = tk.Frame(root, bg="#00d4ff", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="💰 SISTEMA DE PAGOS",
            font=("Segoe UI", 18, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e"
        ).pack(pady=15)
        
        # Info usuario
        user_frame = tk.Frame(root, bg="#ffffff", relief="solid", borderwidth=1)
        user_frame.pack(fill="x", padx=20, pady=(15, 0))
        
        tk.Label(
            user_frame,
            text=f"👤 Usuario: {usuario}  |  📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#666666"
        ).pack(pady=8)
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#ffffff", relief="solid", borderwidth=1)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Monto
        tk.Label(
            main_frame,
            text="Monto (S/.)",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            anchor="w"
        ).pack(pady=(20, 5), padx=20, fill="x")
        
        self.monto_entry = tk.Entry(
            main_frame,
            font=("Segoe UI", 12),
            bg="#f8f9fa",
            relief="solid",
            borderwidth=1
        )
        self.monto_entry.pack(pady=(0, 15), padx=20, fill="x", ipady=8)
        
        # Método de pago
        tk.Label(
            main_frame,
            text="Método de pago",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            anchor="w"
        ).pack(pady=(0, 5), padx=20, fill="x")
        
        style = ttk.Style()
        style.configure("Custom.TCombobox", padding=5)
        
        self.metodo = ttk.Combobox(
            main_frame,
            values=["Tarjeta de Crédito", "PayPal", "Efectivo", "Yape", "Plin"],
            font=("Segoe UI", 11),
            state="readonly",
            style="Custom.TCombobox"
        )
        self.metodo.pack(pady=(0, 15), padx=20, fill="x", ipady=5)
        self.metodo.current(0)
        self.metodo.bind("<<ComboboxSelected>>", self.actualizar_campos_dinamicos)
        
        # --- Frame para campos dinámicos ---
        self.frame_adicional = tk.Frame(main_frame, bg="#ffffff")
        self.frame_adicional.pack(pady=0, padx=20, fill="x")
        
        # Inicializar los campos dinámicos por primera vez
        self.actualizar_campos_dinamicos()

        # Botones
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=10, padx=20, fill="x")
        
        self.pagar_btn = tk.Button(
            button_frame,
            text="💳 REALIZAR PAGO",
            font=("Segoe UI", 12, "bold"),
            bg="#51cf66",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.realizar_pago,
            activebackground="#40c057"
        )
        self.pagar_btn.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 5))
        
        self.limpiar_btn = tk.Button(
            button_frame,
            text="🔄 LIMPIAR",
            font=("Segoe UI", 11, "bold"),
            bg="#868e96",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.limpiar_campos,
            activebackground="#6c757d"
        )
        self.limpiar_btn.pack(side="left", fill="x", expand=True, ipady=10, padx=(5, 0))
        
        # Resultado
        resultado_frame = tk.Frame(main_frame, bg="#e7f5ff", relief="solid", borderwidth=1)
        resultado_frame.pack(pady=15, padx=20, fill="x")
        
        self.resultado_label = tk.Label(
            resultado_frame,
            text="Esperando operación...",
            font=("Segoe UI", 10),
            bg="#e7f5ff",
            fg="#1971c2",
            wraplength=420,
            justify="left"
        )
        self.resultado_label.pack(pady=15, padx=15)
        
        # Botón cerrar sesión
        tk.Button(
            root,
            text="🚪 Cerrar Sesión",
            font=("Segoe UI", 10),
            bg="#ff6b6b",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.cerrar_sesion,
            activebackground="#fa5252"
        ).pack(pady=(0, 15), padx=20, fill="x", ipady=8)
    
    def _crear_campo_adicional(self, label_texto, key, show_char=None):
        """Función helper para crear un par Label-Entry dinámicamente."""
        tk.Label(
            self.frame_adicional,
            text=label_texto,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            anchor="w"
        ).pack(pady=(5, 5), fill="x")
        
        entry = tk.Entry(
            self.frame_adicional,
            font=("Segoe UI", 11),
            bg="#f8f9fa",
            relief="solid",
            borderwidth=1,
            show=show_char
        )
        entry.pack(pady=(0, 10), fill="x", ipady=6)
        
        # Guardar la referencia al entry
        self.campos_adicionales[key] = entry

    def actualizar_campos_dinamicos(self, event=None):
        """Limpia y recrea los campos de entrada según el método de pago."""
        # Limpiar campos anteriores
        for widget in self.frame_adicional.winfo_children():
            widget.destroy()
        self.campos_adicionales.clear()
        
        metodo = self.metodo.get()
        
        if metodo == "Tarjeta de Crédito":
            self._crear_campo_adicional("Número de Tarjeta (16 dígitos)", "numero")
            self._crear_campo_adicional("Nombre del Titular", "titular")
            # Frame para Expiración y CVV
            sub_frame = tk.Frame(self.frame_adicional, bg="#ffffff")
            sub_frame.pack(fill="x")
            
            # Campo Expiración
            tk.Label(sub_frame, text="Exp. (MM/AA)", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, sticky="w")
            exp_entry = tk.Entry(sub_frame, font=("Segoe UI", 11), bg="#f8f9fa", relief="solid", borderwidth=1, width=10)
            exp_entry.grid(row=1, column=0, sticky="w", ipady=6, padx=(0, 10))
            self.campos_adicionales["expiracion"] = exp_entry
            
            # Campo CVV
            tk.Label(sub_frame, text="CVV (3-4 dígitos)", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=1, sticky="w")
            cvv_entry = tk.Entry(sub_frame, font=("Segoe UI", 11), bg="#f8f9fa", relief="solid", borderwidth=1, width=10, show="*")
            cvv_entry.grid(row=1, column=1, sticky="w", ipady=6)
            self.campos_adicionales["cvv"] = cvv_entry
            
        elif metodo == "PayPal":
            self._crear_campo_adicional("Correo electrónico", "correo")
            self._crear_campo_adicional("Nombre Remitente", "nombre_remitente")

        elif metodo in ["Yape", "Plin"]:
            self._crear_campo_adicional("Número de teléfono (9 dígitos)", "numero")
            self._crear_campo_adicional("Nombre Remitente", "nombre_remitente")
            
        elif metodo == "Efectivo":
            self._crear_campo_adicional("Nombre del Cliente", "nombre")
            self._crear_campo_adicional("DNI del Cliente (8 dígitos)", "dni")

    def limpiar_campos(self):
        self.monto_entry.delete(0, tk.END)
        for entry in self.campos_adicionales.values():
            entry.delete(0, tk.END)
        self.metodo.current(0)
        self.actualizar_campos_dinamicos()
        self.resultado_label.config(
            text="Esperando operación...",
            bg="#e7f5ff",
            fg="#1971c2"
        )
    
    def realizar_pago(self):
        try:
            metodo = self.metodo.get()
            monto_texto = self.monto_entry.get().strip()
            
            # --- Validaciones de Monto ---
            if not monto_texto:
                raise ValueError("El monto es obligatorio.")
            monto = float(monto_texto)
            if monto <= 0:
                raise ValueError("El monto debe ser mayor a 0.")

            # --- Recopilar datos dinámicos ---
            datos = {k: v.get().strip() for k, v in self.campos_adicionales.items()}
            pago = None

            # --- Crear objeto y validar campos específicos ---
            if metodo == "Tarjeta de Crédito":
                if not all(k in datos and datos[k] for k in ["numero", "titular", "expiracion", "cvv"]):
                    raise ValueError("Complete todos los campos de la tarjeta.")
                if not re.match(r"^\d{16}$", datos["numero"]):
                    raise ValueError("Número de tarjeta debe tener 16 dígitos.")
                if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", datos["expiracion"]):
                    raise ValueError("Fecha de expiración debe ser MM/AA.")
                if not re.match(r"^\d{3,4}$", datos["cvv"]):
                    raise ValueError("CVV debe tener 3 o 4 dígitos.")
                
                pago = TarjetaCredito(monto, datos["numero"], datos["titular"], datos["expiracion"], datos["cvv"])
            
            elif metodo == "PayPal":
                if not all(k in datos and datos[k] for k in ["correo", "nombre_remitente"]):
                    raise ValueError("Correo y Nombre son obligatorios.")
                if not re.match(r"[^@]+@[^@]+\.[^@]+", datos["correo"]):
                    raise ValueError("Correo electrónico no válido.")
                
                pago = PayPal(monto, datos["correo"], datos["nombre_remitente"])

            elif metodo == "Efectivo":
                if not all(k in datos and datos[k] for k in ["nombre", "dni"]):
                    raise ValueError("Nombre y DNI son obligatorios.")
                if not re.match(r"^\d{8}$", datos["dni"]):
                    raise ValueError("DNI debe tener 8 dígitos.")
                
                pago = Efectivo(monto, datos["nombre"], datos["dni"])

            elif metodo in ["Yape", "Plin"]:
                if not all(k in datos and datos[k] for k in ["numero", "nombre_remitente"]):
                    raise ValueError("Número y Nombre son obligatorios.")
                if not re.match(r"^\d{9}$", datos["numero"]):
                    raise ValueError("Número de teléfono debe tener 9 dígitos.")
                
                if metodo == "Yape":
                    pago = Yape(monto, datos["numero"], datos["nombre_remitente"])
                else:
                    pago = Plin(monto, datos["numero"], datos["nombre_remitente"])
            
            else:
                raise ValueError("Método de pago no reconocido.")

            # --- Procesar Pago y Generar Voucher ---
            resultado = pago.realizar_pago()
            voucher_texto = pago.generar_voucher()
            
            # Mostrar resultado en la app principal
            self.resultado_label.config(
                text=f"✅ {resultado}\n\nProcesado por: {self.usuario}",
                bg="#d3f9d8",
                fg="#2b8a3e"
            )
            
            # Mostrar ventana de voucher
            self.mostrar_voucher(voucher_texto, pago.numero_operacion)
            
            # Limpiar campos después de éxito
            self.limpiar_campos()

        except (ValueError, TypeError) as e:
            # Capturar cualquier error de validación
            messagebox.showerror("❌ Error de Validación", str(e))
            self.resultado_label.config(
                text=f"❌ Error: {e}",
                bg="#ffe3e3",
                fg="#c92a2a"
            )

    def mostrar_voucher(self, voucher_texto, num_operacion):
        """Crea una nueva ventana para mostrar el voucher."""
        
        # Crear la ventana
        voucher_win = tk.Toplevel(self.root)
        voucher_win.title(f"Voucher: {num_operacion}")
        voucher_win.geometry("400x450")
        voucher_win.resizable(False, False)
        voucher_win.configure(bg="#ffffff")
        
        # Hacerla modal (bloquea la ventana principal)
        voucher_win.transient(self.root)
        voucher_win.grab_set()
        
        tk.Label(
            voucher_win,
            text="Voucher Generado Exitosamente",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#003366" # Azul oscuro
        ).pack(pady=10)
        
        # Área de texto para el voucher
        voucher_text = Text(
            voucher_win,
            font=("Courier", 10), # Fuente monoespaciada
            bg="#f8f9fa",
            relief="solid",
            borderwidth=1,
            height=15,
            width=50
        )
        voucher_text.pack(pady=10, padx=20)
        voucher_text.insert(tk.END, voucher_texto)
        voucher_text.config(state="disabled") # Hacerlo de solo lectura
        
        # Frame de botones
        btn_frame = tk.Frame(voucher_win, bg="#ffffff")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        def guardar_voucher():
            """Función para guardar el voucher como .txt"""
            try:
                # Pedir al usuario dónde guardar
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")],
                    initialfile=f"Voucher_{num_operacion}.txt",
                    title="Guardar Voucher"
                )
                
                if filepath: # Si el usuario no canceló
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(voucher_texto)
                    messagebox.showinfo("Guardado", "Voucher guardado exitosamente.", parent=voucher_win)
                    voucher_win.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo:\n{e}", parent=voucher_win)
        
        # Botón Guardar
        tk.Button(
            btn_frame,
            text="🖨️ Guardar como .TXT",
            font=("Segoe UI", 10, "bold"),
            bg="#007bff",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=guardar_voucher
        ).pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 5))
        
        # Botón Cerrar
        tk.Button(
            btn_frame,
            text="Cerrar",
            font=("Segoe UI", 10),
            bg="#6c757d",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=voucher_win.destroy
        ).pack(side="left", expand=True, fill="x", ipady=8, padx=(5, 0))


    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión actual?"):
            self.root.destroy()
            main() # Reinicia el proceso de login


# -----------------------------------
# CONTROLADOR PRINCIPAL (Sin cambios)
# -----------------------------------
def main():
    root = tk.Tk()
    
    def on_login_success(usuario):
        root.destroy()
        root_pagos = tk.Tk()
        VentanaPagos(root_pagos, usuario)
        root_pagos.mainloop()
    
    VentanaLogin(root, on_login_success)
    root.mainloop()


# -----------------------------------
# EJECUCIÓN
# -----------------------------------
if __name__ == "__main__":
    main()
d
