from typing import TypeVar, Generic
import tkinter as tk
from tkinter import ttk, messagebox

T = TypeVar('T', int, float)

class Calculadora(Generic[T]):
    def __init__(self, a: T, b: T):
        try:
            self.a = a
            self.b = b
        except Exception as e:
            raise TypeError(f"Error al asignar valores: {e}")
    
    def sumar(self) -> T:
        try:
            return self.a + self.b
        except Exception as e:
            raise TypeError(f"Error al sumar: {e}")
    
    def restar(self) -> T:
        try:
            return self.a - self.b
        except Exception as e:
            raise TypeError(f"Error al restar: {e}")
    
    def multiplicar(self) -> T:
        try:
            return self.a * self.b
        except Exception as e:
            raise TypeError(f"Error al multiplicar: {e}")
    
    def dividir(self) -> T:
        try:
            if self.b == 0:
                raise ZeroDivisionError("¡No se puede dividir entre cero!")
            return self.a / self.b
        except Exception as e:
            raise TypeError(f"Error al dividir: {e}")


class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Mi Calculadora Mágica 🎨")
        self.root.geometry("500x600")
        self.root.resizable(True, True)  # Permitir redimensionar
        self.root.minsize(450, 550)  # Tamaño mínimo para mantener legibilidad
        
        # Colores alegres y amigables
        color_fondo = '#E8F5E9'  # Verde muy claro
        color_primario = '#4CAF50'  # Verde
        color_titulo = '#2E7D32'  # Verde oscuro
        
        self.root.configure(bg=color_fondo)
        
        # Frame principal con bordes redondeados
        main_frame = tk.Frame(root, bg=color_fondo, padx=30, pady=25)
        main_frame.pack(expand=True, fill='both')
        
        # 🎈 TÍTULO GRANDE Y DIVERTIDO
        titulo = tk.Label(main_frame, text="🌟 MI CALCULADORA 🌟", 
                         font=('Comic Sans MS', 24, 'bold'), 
                         bg=color_fondo, fg=color_titulo)
        titulo.pack(pady=(0, 10))
        
        subtitulo = tk.Label(main_frame, text="¡Aprende matemáticas de forma divertida!", 
                            font=('Comic Sans MS', 11), 
                            bg=color_fondo, fg='#666')
        subtitulo.pack(pady=(0, 25))
        
        # 📝 FRAME PARA ENTRADAS (más grande y colorido)
        entrada_frame = tk.Frame(main_frame, bg='white', bd=3, relief='ridge')
        entrada_frame.pack(pady=(0, 20), padx=10, fill='x')
        
        # Padding interno
        inner_frame = tk.Frame(entrada_frame, bg='white', padx=20, pady=20)
        inner_frame.pack()
        
        # Primer número
        tk.Label(inner_frame, text="🔢 Primer Número:", 
                font=('Comic Sans MS', 13, 'bold'), 
                bg='white', fg=color_titulo).grid(row=0, column=0, sticky='w', pady=10)
        self.entry_a = tk.Entry(inner_frame, font=('Arial', 16), width=18, 
                               bd=3, relief='solid', justify='center')
        self.entry_a.grid(row=0, column=1, pady=10, padx=(15, 0))
        
        # Segundo número
        tk.Label(inner_frame, text="🔢 Segundo Número:", 
                font=('Comic Sans MS', 13, 'bold'), 
                bg='white', fg=color_titulo).grid(row=1, column=0, sticky='w', pady=10)
        self.entry_b = tk.Entry(inner_frame, font=('Arial', 16), width=18, 
                               bd=3, relief='solid', justify='center')
        self.entry_b.grid(row=1, column=1, pady=10, padx=(15, 0))
        
        # Indicador de tipo
        self.tipo_label = tk.Label(inner_frame, text="💡 Escribe tus números arriba", 
                                   font=('Comic Sans MS', 9, 'italic'), 
                                   bg='white', fg='#888')
        self.tipo_label.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        # 🎯 TÍTULO DE OPERACIONES
        tk.Label(main_frame, text="✨ ¿Qué quieres hacer? ✨", 
                font=('Comic Sans MS', 14, 'bold'), 
                bg=color_fondo, fg=color_titulo).pack(pady=(10, 15))
        
        # 🎨 FRAME PARA BOTONES GRANDES Y COLORIDOS
        botones_frame = tk.Frame(main_frame, bg=color_fondo)
        botones_frame.pack(pady=(0, 20))
        
        # Estilo de botones grandes con emojis
        btn_config = {
            'font': ('Comic Sans MS', 14, 'bold'),
            'width': 15,
            'height': 2,
            'bd': 4,
            'relief': 'raised',
            'cursor': 'hand2'
        }
        
        # Primera fila de botones
        btn_sumar = tk.Button(botones_frame, text="➕ SUMAR", 
                             bg='#81C784', fg='white',
                             activebackground='#66BB6A',
                             command=lambda: self.ejecutar_operacion("sumar"), 
                             **btn_config)
        btn_sumar.grid(row=0, column=0, padx=8, pady=8)
        
        btn_restar = tk.Button(botones_frame, text="➖ RESTAR", 
                              bg='#64B5F6', fg='white',
                              activebackground='#42A5F5',
                              command=lambda: self.ejecutar_operacion("restar"), 
                              **btn_config)
        btn_restar.grid(row=0, column=1, padx=8, pady=8)
        
        # Segunda fila de botones
        btn_multiplicar = tk.Button(botones_frame, text="✖️ MULTIPLICAR", 
                                   bg='#FFB74D', fg='white',
                                   activebackground='#FFA726',
                                   command=lambda: self.ejecutar_operacion("multiplicar"), 
                                   **btn_config)
        btn_multiplicar.grid(row=1, column=0, padx=8, pady=8)
        
        btn_dividir = tk.Button(botones_frame, text="➗ DIVIDIR", 
                               bg='#E57373', fg='white',
                               activebackground='#EF5350',
                               command=lambda: self.ejecutar_operacion("dividir"), 
                               **btn_config)
        btn_dividir.grid(row=1, column=1, padx=8, pady=8)
        
        # 🏆 ÁREA DE RESULTADO (grande y visible)
        resultado_frame = tk.Frame(main_frame, bg='#FFF9C4', bd=3, relief='solid')
        resultado_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        tk.Label(resultado_frame, text="🎉 RESULTADO:", 
                font=('Comic Sans MS', 12, 'bold'), 
                bg='#FFF9C4', fg='#F57F17').pack(pady=(10, 5))
        
        self.resultado_label = tk.Label(resultado_frame, text="", 
                                       font=('Arial', 20, 'bold'),
                                       bg='#FFF9C4', fg='#388E3C',
                                       height=2)
        self.resultado_label.pack(pady=(0, 10))
        
        # Efectos hover para botones
        for btn in [btn_sumar, btn_restar, btn_multiplicar, btn_dividir]:
            btn.bind('<Enter>', lambda e, b=btn: b.config(relief='sunken'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(relief='raised'))
    
    def ejecutar_operacion(self, operacion):
        try:
            # Obtener valores
            str_a = self.entry_a.get().strip()
            str_b = self.entry_b.get().strip()
            
            if not str_a or not str_b:
                messagebox.showwarning("⚠️ ¡Ups!", 
                                      "¡No olvides escribir los dos números! 😊")
                return
            
            # Detectar tipo automáticamente
            if '.' not in str_a and '.' not in str_b:
                a = int(str_a)
                b = int(str_b)
                calc = Calculadora[int](a, b)
                tipo_detectado = "números enteros"
            else:
                a = float(str_a)
                b = float(str_b)
                calc = Calculadora[float](a, b)
                tipo_detectado = "números decimales"
            
            # Actualizar tipo detectado
            self.tipo_label.config(text=f"✅ Usando {tipo_detectado}", fg='#4CAF50')
            
            # Ejecutar operación
            if operacion == "sumar":
                resultado = calc.sumar()
                emoji = "🎉"
                operacion_texto = "Suma"
            elif operacion == "restar":
                resultado = calc.restar()
                emoji = "⭐"
                operacion_texto = "Resta"
            elif operacion == "multiplicar":
                resultado = calc.multiplicar()
                emoji = "🌟"
                operacion_texto = "Multiplicación"
            elif operacion == "dividir":
                resultado = calc.dividir()
                emoji = "✨"
                operacion_texto = "División"
            
            # Mostrar resultado grande
            self.resultado_label.config(text=f"{resultado}", fg='#2E7D32')
            
            # Mensaje de felicitación
            messagebox.showinfo(f"{emoji} ¡Muy bien!", 
                              f"{operacion_texto}:\n\n"
                              f"{a} y {b} = {resultado}\n\n"
                              f"¡Excelente trabajo! 🎊")
            
        except ValueError:
            self.resultado_label.config(text="❌", fg='#D32F2F')
            self.tipo_label.config(text="💡 Escribe tus números arriba", fg='#888')
            messagebox.showerror("❌ ¡Error!", 
                               "Por favor escribe solo números.\n\n"
                               "Ejemplo: 5 o 3.14 😊")
        except ZeroDivisionError:
            self.resultado_label.config(text="⚠️", fg='#F57C00')
            messagebox.showerror("⚠️ ¡Cuidado!", 
                               "¡No se puede dividir entre cero!\n\n"
                               "Intenta con otro número. 😊")
        except Exception as e:
            self.resultado_label.config(text="❌", fg='#D32F2F')
            self.tipo_label.config(text="💡 Escribe tus números arriba", fg='#888')
            messagebox.showerror("❌ ¡Error!", 
                               f"Algo salió mal:\n{str(e)}\n\n"
                               "¡Inténtalo de nuevo! 😊")


# Crear y ejecutar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = CalculadoraApp(ventana)
    ventana.mainloop()
