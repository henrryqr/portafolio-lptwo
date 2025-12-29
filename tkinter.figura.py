import tkinter as tk
from tkinter import ttk
import math

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
        self.root.title("Calculadora de Áreas")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title = ttk.Label(main_frame, text="Calculadora de Áreas de Figuras", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Selección de figura
        ttk.Label(main_frame, text="Selecciona una figura:", 
                 font=("Arial", 11)).grid(row=1, column=0, columnspan=2, pady=10)
        
        self.figura_var = tk.StringVar(value="Cuadrado")
        figuras = ["Cuadrado", "Círculo", "Triángulo"]
        
        for i, figura in enumerate(figuras):
            ttk.Radiobutton(main_frame, text=figura, variable=self.figura_var, 
                           value=figura, command=self.cambiar_figura).grid(
                           row=2, column=i, padx=10, pady=5)
        
        # Frame para inputs
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Botón calcular
        ttk.Button(main_frame, text="Calcular Área", 
                  command=self.calcular_area).grid(row=4, column=0, columnspan=3, pady=10)
        
        # Resultado
        self.resultado_label = ttk.Label(main_frame, text="", 
                                        font=("Arial", 14, "bold"), 
                                        foreground="blue")
        self.resultado_label.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Historial
        ttk.Label(main_frame, text="Historial:", 
                 font=("Arial", 11, "bold")).grid(row=6, column=0, columnspan=3, pady=(20,5))
        
        self.historial_text = tk.Text(main_frame, height=8, width=50, state='disabled')
        self.historial_text.grid(row=7, column=0, columnspan=3, pady=5)
        
        # Inicializar campos
        self.cambiar_figura()
    
    def cambiar_figura(self):
        # Limpiar frame de inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        figura = self.figura_var.get()
        
        if figura == "Cuadrado":
            ttk.Label(self.input_frame, text="Lado:").grid(row=0, column=0, padx=5)
            self.entrada1 = ttk.Entry(self.input_frame, width=15)
            self.entrada1.grid(row=0, column=1, padx=5)
            
        elif figura == "Círculo":
            ttk.Label(self.input_frame, text="Radio:").grid(row=0, column=0, padx=5)
            self.entrada1 = ttk.Entry(self.input_frame, width=15)
            self.entrada1.grid(row=0, column=1, padx=5)
            
        elif figura == "Triángulo":
            ttk.Label(self.input_frame, text="Base:").grid(row=0, column=0, padx=5)
            self.entrada1 = ttk.Entry(self.input_frame, width=15)
            self.entrada1.grid(row=0, column=1, padx=5)
            
            ttk.Label(self.input_frame, text="Altura:").grid(row=1, column=0, padx=5, pady=5)
            self.entrada2 = ttk.Entry(self.input_frame, width=15)
            self.entrada2.grid(row=1, column=1, padx=5, pady=5)
    
    def calcular_area(self):
        try:
            figura_tipo = self.figura_var.get()
            
            if figura_tipo == "Cuadrado":
                lado = float(self.entrada1.get())
                figura = Cuadrado(lado)
                area = figura.area()
                mensaje = f"Área del Cuadrado (lado={lado}): {area:.2f}"
                
            elif figura_tipo == "Círculo":
                radio = float(self.entrada1.get())
                figura = Circulo(radio)
                area = figura.area()
                mensaje = f"Área del Círculo (radio={radio}): {area:.2f}"
                
            elif figura_tipo == "Triángulo":
                base = float(self.entrada1.get())
                altura = float(self.entrada2.get())
                figura = Triangulo(base, altura)
                area = figura.area()
                mensaje = f"Área del Triángulo (base={base}, altura={altura}): {area:.2f}"
            
            self.resultado_label.config(text=f"Área: {area:.2f}")
            
            # Agregar al historial
            self.historial_text.config(state='normal')
            self.historial_text.insert('1.0', mensaje + '\n')
            self.historial_text.config(state='disabled')
            
        except ValueError:
            self.resultado_label.config(text="Error: Ingresa valores numéricos válidos", 
                                       foreground="red")

# Crear ventana principal
root = tk.Tk()
app = CalculadoraAreas(root)
root.mainloop()
