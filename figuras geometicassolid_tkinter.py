import tkinter as tk
from tkinter import ttk
import math

# Principio S 
class FiguraGeometrica:
    def area(self):
        raise NotImplementedError("Debe implementar el metodo area")
    def perimetro(self):
        raise NotImplementedError("Debe implementar el metodo perimetro")

# Principio O y L 
class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio
    def area(self):
        return math.pi * (self.radio ** 2)
    def perimetro(self):
        return 2 * math.pi * self.radio

class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    def area(self):
        return self.base * self.altura
    def perimetro(self):
        return 2 * (self.base + self.altura)

# Principio D 
class Figura:
    def __init__(self, figura: FiguraGeometrica):
        self.figura = figura
    def ejecutar(self):
        return f"Área: {self.figura.area():.2f}\nPerímetro: {self.figura.perimetro():.2f}"

# Interfaz Tkinter
class AplicacionFiguras:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Figuras Geométricas")
        self.root.geometry("520x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f4f8')
        
        # Estilos personalizados
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores profesionales
        self.color_primary = '#2563eb'
        self.color_secondary = '#1e40af'
        self.color_bg = '#ffffff'
        self.color_text = '#1f2937'
        self.color_success = '#10b981'
        
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.color_primary,
                       background='#f0f4f8')
        
        style.configure('Card.TFrame',
                       background=self.color_bg,
                       relief='flat')
        
        style.configure('Custom.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.color_text,
                       background=self.color_bg,
                       padding=5)
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.color_text,
                       background=self.color_bg)
        
        style.configure('Custom.TCombobox',
                       fieldbackground=self.color_bg,
                       font=('Segoe UI', 10))
        
        style.configure('Calc.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='white',
                       background=self.color_primary,
                       borderwidth=0,
                       padding=(20, 10))
        
        style.map('Calc.TButton',
                 background=[('active', self.color_secondary)])
        
        # Frame principal con padding
        main_frame = tk.Frame(root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título principal
        titulo = ttk.Label(main_frame, 
                          text="Calculadora de Figuras",
                          style='Title.TLabel')
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(main_frame,
                             text="Calcula áreas y perímetros de forma precisa",
                             font=('Segoe UI', 10),
                             foreground='#6b7280',
                             background='#f0f4f8')
        subtitulo.pack(pady=(0, 25))
        
        # Card principal
        card = ttk.Frame(main_frame, style='Card.TFrame', relief='solid', borderwidth=1)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Contenido del card con padding
        content = tk.Frame(card, bg=self.color_bg)
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Selector de figura
        selector_frame = tk.Frame(content, bg=self.color_bg)
        selector_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(selector_frame, 
                 text="Tipo de figura",
                 style='Header.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        self.tipo_figura = tk.StringVar(value="Círculo")
        combo = ttk.Combobox(selector_frame, 
                            textvariable=self.tipo_figura,
                            values=["Círculo", "Rectángulo"],
                            state="readonly",
                            font=('Segoe UI', 10),
                            width=30,
                            style='Custom.TCombobox')
        combo.pack(fill=tk.X, ipady=5)
        combo.bind("<<ComboboxSelected>>", self.cambiar_figura)
        
        # Separador
        sep1 = tk.Frame(content, height=1, bg='#e5e7eb')
        sep1.pack(fill=tk.X, pady=20)
        
        # Frame para parámetros
        params_container = tk.Frame(content, bg=self.color_bg)
        params_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame para parámetros del círculo
        self.frame_circulo = tk.Frame(params_container, bg=self.color_bg)
        self.frame_circulo.pack(fill=tk.X)
        
        ttk.Label(self.frame_circulo,
                 text="Radio (r)",
                 style='Header.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        self.radio_entry = tk.Entry(self.frame_circulo,
                                    font=('Segoe UI', 11),
                                    bg='#f9fafb',
                                    fg=self.color_text,
                                    relief='solid',
                                    borderwidth=1,
                                    highlightthickness=2,
                                    highlightbackground='#e5e7eb',
                                    highlightcolor=self.color_primary)
        self.radio_entry.pack(fill=tk.X, ipady=8)
        self.radio_entry.insert(0, "4")
        
        # Frame para parámetros del rectángulo
        self.frame_rectangulo = tk.Frame(params_container, bg=self.color_bg)
        
        ttk.Label(self.frame_rectangulo,
                 text="Base (b)",
                 style='Header.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        self.base_entry = tk.Entry(self.frame_rectangulo,
                                   font=('Segoe UI', 11),
                                   bg='#f9fafb',
                                   fg=self.color_text,
                                   relief='solid',
                                   borderwidth=1,
                                   highlightthickness=2,
                                   highlightbackground='#e5e7eb',
                                   highlightcolor=self.color_primary)
        self.base_entry.pack(fill=tk.X, ipady=8)
        self.base_entry.insert(0, "3")
        
        ttk.Label(self.frame_rectangulo,
                 text="Altura (h)",
                 style='Header.TLabel').pack(anchor=tk.W, pady=(15, 8))
        
        self.altura_entry = tk.Entry(self.frame_rectangulo,
                                     font=('Segoe UI', 11),
                                     bg='#f9fafb',
                                     fg=self.color_text,
                                     relief='solid',
                                     borderwidth=1,
                                     highlightthickness=2,
                                     highlightbackground='#e5e7eb',
                                     highlightcolor=self.color_primary)
        self.altura_entry.pack(fill=tk.X, ipady=8)
        self.altura_entry.insert(0, "4")
        
        # Separador
        sep2 = tk.Frame(content, height=1, bg='#e5e7eb')
        sep2.pack(fill=tk.X, pady=25)
        
        # Botón calcular con hover effect
        btn_frame = tk.Frame(content, bg=self.color_bg)
        btn_frame.pack(fill=tk.X)
        
        self.btn_calcular = tk.Button(btn_frame,
                                      text="Calcular",
                                      font=('Segoe UI', 12, 'bold'),
                                      bg=self.color_primary,
                                      fg='white',
                                      relief='flat',
                                      cursor='hand2',
                                      borderwidth=0,
                                      command=self.calcular)
        self.btn_calcular.pack(fill=tk.X, ipady=12)
        
        # Efectos hover para el botón
        self.btn_calcular.bind('<Enter>', lambda e: self.btn_calcular.config(bg=self.color_secondary))
        self.btn_calcular.bind('<Leave>', lambda e: self.btn_calcular.config(bg=self.color_primary))
        
        # Área de resultados
        results_frame = tk.Frame(content, bg=self.color_bg)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(25, 0))
        
        ttk.Label(results_frame,
                 text="Resultados",
                 style='Header.TLabel').pack(anchor=tk.W, pady=(0, 12))
        
        # Card de resultados
        result_card = tk.Frame(results_frame, bg='#f9fafb', relief='solid', borderwidth=1)
        result_card.pack(fill=tk.BOTH, expand=True)
        
        self.resultado_text = tk.Text(result_card,
                                     height=4,
                                     font=('Segoe UI', 11),
                                     bg='#f9fafb',
                                     fg=self.color_text,
                                     relief='flat',
                                     borderwidth=0,
                                     padx=15,
                                     pady=15,
                                     wrap=tk.WORD)
        self.resultado_text.pack(fill=tk.BOTH, expand=True)
        self.resultado_text.insert(1.0, "Los resultados aparecerán aquí...")
        self.resultado_text.config(state=tk.DISABLED)
    
    def cambiar_figura(self, event=None):
        if self.tipo_figura.get() == "Círculo":
            self.frame_rectangulo.pack_forget()
            self.frame_circulo.pack(fill=tk.X)
        else:
            self.frame_circulo.pack_forget()
            self.frame_rectangulo.pack(fill=tk.X)
    
    def calcular(self):
        try:
            if self.tipo_figura.get() == "Círculo":
                radio = float(self.radio_entry.get())
                if radio <= 0:
                    raise ValueError("El radio debe ser positivo")
                figura_obj = Circulo(radio)
                figura_nombre = "Círculo"
            else:
                base = float(self.base_entry.get())
                altura = float(self.altura_entry.get())
                if base <= 0 or altura <= 0:
                    raise ValueError("Las dimensiones deben ser positivas")
                figura_obj = Rectangulo(base, altura)
                figura_nombre = "Rectángulo"
            
            figura = Figura(figura_obj)
            area = figura.figura.area()
            perimetro = figura.figura.perimetro()
            
            resultado = f"📐 {figura_nombre}\n\n"
            resultado += f"Área: {area:.2f} unidades²\n"
            resultado += f"Perímetro: {perimetro:.2f} unidades"
            
            self.resultado_text.config(state=tk.NORMAL, fg=self.color_success)
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(1.0, resultado)
            self.resultado_text.config(state=tk.DISABLED)
            
        except ValueError as e:
            mensaje_error = str(e) if str(e) else "Ingrese valores numéricos válidos y positivos"
            self.resultado_text.config(state=tk.NORMAL, fg='#ef4444')
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(1.0, f"❌ Error\n\n{mensaje_error}")
            self.resultado_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionFiguras(root)
    root.mainloop()
