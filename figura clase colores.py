import tkinter as tk
from tkinter import ttk, messagebox
import math

# Constantes para colores y estilos
BG_COLOR = "#2C3E50"
FRAME_BG = "#34495E"
TEXT_COLOR = "#ECF0F1"
BUTTON_ACTIVE_BG = "#E67E22"
ERROR_BG = "#E74C3C"
SUCCESS_BG = "#16A085"

class Figura:
    def area(self):
        pass

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado
    def area(self):
        return self.lado ** 2

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio
    def area(self):
        return math.pi * (self.radio ** 2)

class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    def area(self):
        return (self.base * self.altura) / 2

class CalculadoraAreas:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Áreas - Versión Profesional")
        self.root.geometry("950x850")
        self.root.resizable(True, True)  # Permitir redimensionar para mejor usabilidad
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(800, 700)  # Tamaño mínimo
        
        # Estilo ttk para widgets modernos
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        style.configure("TLabel", font=("Arial", 12), background=FRAME_BG, foreground=TEXT_COLOR)
        style.configure("TEntry", font=("Arial", 12), padding=5)
        style.configure("TRadiobutton", font=("Arial", 12, "bold"), background=FRAME_BG, foreground=TEXT_COLOR)
        
        # Frame principal
        main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(main_frame, text="🔷 Calculadora de Áreas 🔷", 
                        font=("Arial", 28, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title.pack(pady=20)
        
        # Frame de selección
        select_frame = tk.Frame(main_frame, bg=FRAME_BG, relief=tk.RAISED, bd=3)
        select_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(select_frame, text="Selecciona una figura:", 
                font=("Arial", 16, "bold"), bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=15)
        
        self.figura_var = tk.StringVar(value="Cuadrado")
        
        buttons_frame = tk.Frame(select_frame, bg=FRAME_BG)
        buttons_frame.pack(pady=10)
        
        # Botones de figuras con colores y ttk
        self.btn_cuadrado = ttk.Radiobutton(buttons_frame, text="⬛ Cuadrado", 
                                           variable=self.figura_var, value="Cuadrado",
                                           command=self.cambiar_figura)
        self.btn_cuadrado.pack(side=tk.LEFT, padx=10)
        
        self.btn_circulo = ttk.Radiobutton(buttons_frame, text="⚫ Círculo", 
                                          variable=self.figura_var, value="Círculo",
                                          command=self.cambiar_figura)
        self.btn_circulo.pack(side=tk.LEFT, padx=10)
        
        self.btn_triangulo = ttk.Radiobutton(buttons_frame, text="🔺 Triángulo", 
                                            variable=self.figura_var, value="Triángulo",
                                            command=self.cambiar_figura)
        self.btn_triangulo.pack(side=tk.LEFT, padx=10)
        
        # Frame para inputs
        self.input_frame = tk.Frame(main_frame, bg=FRAME_BG, relief=tk.RAISED, bd=3)
        self.input_frame.pack(pady=15, padx=20, fill=tk.X)
        
        # Canvas para dibujar
        canvas_frame = tk.Frame(main_frame, bg=TEXT_COLOR, relief=tk.SUNKEN, bd=3)
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame para botones de acción
        action_frame = tk.Frame(main_frame, bg=BG_COLOR)
        action_frame.pack(pady=10)
        
        # Botón calcular
        calc_button = ttk.Button(action_frame, text="🧮 CALCULAR ÁREA", 
                                command=self.calcular_area)
        calc_button.pack(side=tk.LEFT, padx=10)
        
        # Botón limpiar
        clear_button = ttk.Button(action_frame, text="🗑️ LIMPIAR", 
                                 command=self.limpiar)
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # Resultado
        self.resultado_label = tk.Label(main_frame, text="Área: ---", 
                                       font=("Arial", 18, "bold"), 
                                       bg=SUCCESS_BG, fg="white", relief=tk.RAISED,
                                       bd=4, padx=30, pady=15)
        self.resultado_label.pack(pady=15, fill=tk.X)
        
        # Inicializar
        self.cambiar_figura()
    
    def cambiar_figura(self):
        # Limpiar frame de inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        figura = self.figura_var.get()
        
        # Label de parámetros
        tk.Label(self.input_frame, text="Parámetros:", font=("Arial", 14, "bold"),
                bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=15)
        
        inputs_container = tk.Frame(self.input_frame, bg=FRAME_BG)
        inputs_container.pack(pady=15)
        
        if figura == "Cuadrado":
            tk.Label(inputs_container, text="Lado (unidades):", font=("Arial", 12, "bold"),
                    bg=FRAME_BG, fg="#E74C3C").grid(row=0, column=0, padx=8, pady=8, sticky="e")
            self.entrada1 = ttk.Entry(inputs_container, width=20)
            self.entrada1.grid(row=0, column=1, padx=8, pady=8)
            self.dibujar_cuadrado()
            
        elif figura == "Círculo":
            tk.Label(inputs_container, text="Radio (unidades):", font=("Arial", 12, "bold"),
                    bg=FRAME_BG, fg="#3498DB").grid(row=0, column=0, padx=8, pady=8, sticky="e")
            self.entrada1 = ttk.Entry(inputs_container, width=20)
            self.entrada1.grid(row=0, column=1, padx=8, pady=8)
            self.dibujar_circulo()
            
        elif figura == "Triángulo":
            tk.Label(inputs_container, text="Base (unidades):", font=("Arial", 12, "bold"),
                    bg=FRAME_BG, fg="#2ECC71").grid(row=0, column=0, padx=8, pady=8, sticky="e")
            self.entrada1 = ttk.Entry(inputs_container, width=20)
            self.entrada1.grid(row=0, column=1, padx=8, pady=8)
            
            tk.Label(inputs_container, text="Altura (unidades):", font=("Arial", 12, "bold"),
                    bg=FRAME_BG, fg="#2ECC71").grid(row=1, column=0, padx=8, pady=8, sticky="e")
            self.entrada2 = ttk.Entry(inputs_container, width=20)
            self.entrada2.grid(row=1, column=1, padx=8, pady=8)
            self.dibujar_triangulo()
    
    def dibujar_cuadrado(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1: width = 450  # Valor por defecto si no está renderizado
        if height <= 1: height = 300
        x, y = width // 2 - 75, height // 2 - 75
        size = 150
        self.canvas.create_rectangle(x, y, x+size, y+size, 
                                     fill="#E74C3C", outline="#C0392B", width=4)
        self.canvas.create_text(width // 2, height - 30, text="Cuadrado", 
                               font=("Arial", 16, "bold"), fill="#E74C3C")
    
    def dibujar_circulo(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1: width = 450
        if height <= 1: height = 300
        x, y = width // 2, height // 2
        r = 90
        self.canvas.create_oval(x-r, y-r, x+r, y+r, 
                               fill="#3498DB", outline="#2980B9", width=4)
        self.canvas.create_text(width // 2, height - 30, text="Círculo", 
                               font=("Arial", 16, "bold"), fill="#3498DB")
    
    def dibujar_triangulo(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1: width = 450
        if height <= 1: height = 300
        x, y = width // 2, height // 2 - 75
        points = [x, y, x-105, y+150, x+105, y+150]
        self.canvas.create_polygon(points, fill="#2ECC71", 
                                  outline="#27AE60", width=4)
        self.canvas.create_text(width // 2, height - 30, text="Triángulo", 
                               font=("Arial", 16, "bold"), fill="#2ECC71")
    
    def calcular_area(self):
        try:
            figura_tipo = self.figura_var.get()
            
            if figura_tipo == "Cuadrado":
                lado = float(self.entrada1.get())
                if lado <= 0:
                    raise ValueError("El lado debe ser un número positivo.")
                figura = Cuadrado(lado)
                area = figura.area()
                self.resultado_label.config(text=f"Área: {area:.2f} unidades²",
                                          bg="#E74C3C")
                
            elif figura_tipo == "Círculo":
                radio = float(self.entrada1.get())
                if radio <= 0:
                    raise ValueError("El radio debe ser un número positivo.")
                figura = Circulo(radio)
                area = figura.area()
                self.resultado_label.config(text=f"Área: {area:.2f} unidades²",
                                          bg="#3498DB")
                
            elif figura_tipo == "Triángulo":
                base = float(self.entrada1.get())
                altura = float(self.entrada2.get())
                if base <= 0 or altura <= 0:
                    raise ValueError("Base y altura deben ser números positivos.")
                figura = Triangulo(base, altura)
                area = figura.area()
                self.resultado_label.config(text=f"Área: {area:.2f} unidades²",
                                          bg="#2ECC71")
            
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            self.resultado_label.config(text="Área: ---", bg=SUCCESS_BG)
    
    def limpiar(self):
        # Limpiar entradas
        if hasattr(self, 'entrada1'):
            self.entrada1.delete(0, tk.END)
        if hasattr(self, 'entrada2'):
            self.entrada2.delete(0, tk.END)
        self.resultado_label.config(text="Área: ---", bg=SUCCESS_BG)

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraAreas(root)
    root.mainloop()

