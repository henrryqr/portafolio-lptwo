import tkinter as tk
from tkinter import messagebox, Canvas
import math

class FiguraGeometrica:
    def area(self):
        raise NotImplementedError("El método area() debe ser implementado en la subclase")
    
    def perimetro(self):
        raise NotImplementedError("El método perimetro() debe ser implementado en la subclase")

class Rectangulo(FiguraGeometrica):
    def __init__(self, base: float, altura: float):
        if base <= 0 or altura <= 0:
            raise ValueError("La base y la altura deben ser mayores que cero")
        self.base = base
        self.altura = altura
    
    def area(self) -> float:
        return self.base * self.altura
    
    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

class Circulo(FiguraGeometrica):
    def __init__(self, radio: float):
        if radio <= 0:
            raise ValueError("El radio debe ser mayor que cero")
        self.radio = radio
    
    def area(self) -> float:
        return math.pi * (self.radio ** 2)
    
    def perimetro(self) -> float:
        return 2 * math.pi * self.radio


class FigurasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Calculadora de Figuras Geométricas 🎨")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(750, 650)
        
        # Colores alegres
        color_fondo = '#FFF3E0'
        color_primario = '#FF9800'
        color_titulo = '#E65100'
        
        self.root.configure(bg=color_fondo)
        
        # Variables para animación
        self.puntos_totales = 0
        self.calculos_realizados = 0
        self.color_actual = 0
        self.colores_animacion = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(root, bg=color_fondo, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Columna izquierda (controles)
        left_frame = tk.Frame(main_frame, bg=color_fondo)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Columna derecha (visualización)
        right_frame = tk.Frame(main_frame, bg=color_fondo)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # 🎈 TÍTULO
        titulo = tk.Label(left_frame, text="📐 FIGURAS MÁGICAS 📐", 
                         font=('Comic Sans MS', 22, 'bold'), 
                         bg=color_fondo, fg=color_titulo)
        titulo.pack(pady=(0, 5))
        
        subtitulo = tk.Label(left_frame, text="¡Calcula y visualiza!", 
                            font=('Comic Sans MS', 11), 
                            bg=color_fondo, fg='#666')
        subtitulo.pack(pady=(0, 15))
        
        # 🏆 CONTADOR DE PUNTOS
        puntos_frame = tk.Frame(left_frame, bg='#FFD700', bd=3, relief='raised')
        puntos_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(puntos_frame, text="⭐", font=('Arial', 20), 
                bg='#FFD700').pack(side='left', padx=(10, 5))
        
        self.label_puntos = tk.Label(puntos_frame, text="Puntos: 0", 
                                     font=('Comic Sans MS', 14, 'bold'),
                                     bg='#FFD700', fg='#D35400')
        self.label_puntos.pack(side='left', padx=5)
        
        tk.Label(puntos_frame, text="🎯", font=('Arial', 20), 
                bg='#FFD700').pack(side='left', padx=(15, 5))
        
        self.label_calculos = tk.Label(puntos_frame, text="Cálculos: 0", 
                                       font=('Comic Sans MS', 12),
                                       bg='#FFD700', fg='#7D3C98')
        self.label_calculos.pack(side='left', padx=5, pady=10)
        
        # 🔷 SELECTOR DE FIGURA
        selector_frame = tk.Frame(left_frame, bg='white', bd=3, relief='ridge')
        selector_frame.pack(pady=(0, 15), fill='x')
        
        inner_selector = tk.Frame(selector_frame, bg='white', padx=15, pady=12)
        inner_selector.pack()
        
        tk.Label(inner_selector, text="🎯 Elige tu figura:", 
                font=('Comic Sans MS', 12, 'bold'), 
                bg='white', fg=color_titulo).pack()
        
        self.figura_var = tk.StringVar(value="rectangulo")
        
        opciones_frame = tk.Frame(inner_selector, bg='white')
        opciones_frame.pack(pady=(8, 0))
        
        tk.Radiobutton(opciones_frame, text="🟦 Rectángulo", 
                      variable=self.figura_var, value="rectangulo",
                      font=('Comic Sans MS', 11), bg='white',
                      command=self.cambiar_figura,
                      cursor='hand2').pack(side='left', padx=12)
        
        tk.Radiobutton(opciones_frame, text="🔵 Círculo", 
                      variable=self.figura_var, value="circulo",
                      font=('Comic Sans MS', 11), bg='white',
                      command=self.cambiar_figura,
                      cursor='hand2').pack(side='left', padx=12)
        
        # 📝 FRAME PARA ENTRADAS
        self.entrada_frame = tk.Frame(left_frame, bg='white', bd=3, relief='ridge')
        self.entrada_frame.pack(pady=(0, 15), fill='x')
        
        self.inner_entrada = tk.Frame(self.entrada_frame, bg='white', padx=15, pady=15)
        self.inner_entrada.pack()
        
        # Entradas para rectángulo
        self.label_base = tk.Label(self.inner_entrada, text="📏 Base:", 
                                   font=('Comic Sans MS', 12, 'bold'), 
                                   bg='white', fg=color_titulo)
        self.label_base.grid(row=0, column=0, sticky='w', pady=8)
        
        self.entry_base = tk.Entry(self.inner_entrada, font=('Arial', 14), 
                                   width=12, bd=3, relief='solid', justify='center')
        self.entry_base.grid(row=0, column=1, pady=8, padx=(10, 0))
        self.entry_base.bind('<KeyRelease>', self.vista_previa)
        
        self.label_altura = tk.Label(self.inner_entrada, text="📏 Altura:", 
                                     font=('Comic Sans MS', 12, 'bold'), 
                                     bg='white', fg=color_titulo)
        self.label_altura.grid(row=1, column=0, sticky='w', pady=8)
        
        self.entry_altura = tk.Entry(self.inner_entrada, font=('Arial', 14), 
                                     width=12, bd=3, relief='solid', justify='center')
        self.entry_altura.grid(row=1, column=1, pady=8, padx=(10, 0))
        self.entry_altura.bind('<KeyRelease>', self.vista_previa)
        
        # Entrada para círculo
        self.label_radio = tk.Label(self.inner_entrada, text="⭕ Radio:", 
                                    font=('Comic Sans MS', 12, 'bold'), 
                                    bg='white', fg=color_titulo)
        
        self.entry_radio = tk.Entry(self.inner_entrada, font=('Arial', 14), 
                                    width=12, bd=3, relief='solid', justify='center')
        self.entry_radio.bind('<KeyRelease>', self.vista_previa)
        
        # 🎯 BOTÓN DE CALCULAR
        btn_calcular = tk.Button(left_frame, text="🔍 CALCULAR", 
                                font=('Comic Sans MS', 14, 'bold'),
                                bg='#66BB6A', fg='white',
                                activebackground='#4CAF50',
                                width=18, height=2,
                                bd=4, relief='raised',
                                cursor='hand2',
                                command=self.calcular)
        btn_calcular.pack(pady=(0, 15))
        
        btn_calcular.bind('<Enter>', lambda e: btn_calcular.config(relief='sunken', bg='#4CAF50'))
        btn_calcular.bind('<Leave>', lambda e: btn_calcular.config(relief='raised', bg='#66BB6A'))
        
        # 🎨 BOTÓN LIMPIAR
        btn_limpiar = tk.Button(left_frame, text="🗑️ LIMPIAR TODO", 
                               font=('Comic Sans MS', 11),
                               bg='#EF5350', fg='white',
                               activebackground='#E53935',
                               width=18,
                               bd=3, relief='raised',
                               cursor='hand2',
                               command=self.limpiar_todo)
        btn_limpiar.pack()
        
        btn_limpiar.bind('<Enter>', lambda e: btn_limpiar.config(relief='sunken'))
        btn_limpiar.bind('<Leave>', lambda e: btn_limpiar.config(relief='raised'))
        
        # 🏆 ÁREA DE RESULTADOS (columna izquierda)
        resultado_frame = tk.Frame(left_frame, bg='#E1F5FE', bd=3, relief='solid')
        resultado_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(resultado_frame, text="🎉 RESULTADOS:", 
                font=('Comic Sans MS', 11, 'bold'), 
                bg='#E1F5FE', fg='#01579B').pack(pady=(12, 8))
        
        # Área
        area_frame = tk.Frame(resultado_frame, bg='#E1F5FE')
        area_frame.pack(pady=4)
        
        tk.Label(area_frame, text="📊 Área:", 
                font=('Comic Sans MS', 10, 'bold'), 
                bg='#E1F5FE', fg='#0277BD').pack(side='left', padx=(0, 8))
        
        self.resultado_area = tk.Label(area_frame, text="---", 
                                       font=('Arial', 14, 'bold'),
                                       bg='#E1F5FE', fg='#1976D2')
        self.resultado_area.pack(side='left')
        
        # Perímetro
        perimetro_frame = tk.Frame(resultado_frame, bg='#E1F5FE')
        perimetro_frame.pack(pady=4)
        
        tk.Label(perimetro_frame, text="📐 Perímetro:", 
                font=('Comic Sans MS', 10, 'bold'), 
                bg='#E1F5FE', fg='#0277BD').pack(side='left', padx=(0, 8))
        
        self.resultado_perimetro = tk.Label(perimetro_frame, text="---", 
                                           font=('Arial', 14, 'bold'),
                                           bg='#E1F5FE', fg='#1976D2')
        self.resultado_perimetro.pack(side='left')
        
        tk.Label(resultado_frame, text="", bg='#E1F5FE').pack(pady=(0, 12))
        
        # ========== COLUMNA DERECHA: VISUALIZACIÓN ==========
        
        visual_title = tk.Label(right_frame, text="🎨 VISUALIZACIÓN EN VIVO", 
                               font=('Comic Sans MS', 16, 'bold'), 
                               bg=color_fondo, fg=color_titulo)
        visual_title.pack(pady=(0, 10))
        
        # Canvas para dibujar
        canvas_frame = tk.Frame(right_frame, bg='white', bd=4, relief='sunken')
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = Canvas(canvas_frame, bg='#F0F8FF', width=320, height=400)
        self.canvas.pack(padx=10, pady=10)
        
        # Texto de ayuda inicial
        self.canvas.create_text(160, 200, 
                               text="✏️ Escribe los valores\npara ver la figura aquí",
                               font=('Comic Sans MS', 12),
                               fill='#999', tags='ayuda')
        
        # 🎁 MENSAJES MOTIVADORES
        mensajes_frame = tk.Frame(right_frame, bg='#FFEBEE', bd=3, relief='groove')
        mensajes_frame.pack(fill='x', pady=(10, 0))
        
        self.label_mensaje = tk.Label(mensajes_frame, 
                                      text="¡Bienvenido! Elige una figura para empezar 🌟",
                                      font=('Comic Sans MS', 10, 'italic'),
                                      bg='#FFEBEE', fg='#C62828',
                                      wraplength=300, justify='center')
        self.label_mensaje.pack(pady=12, padx=10)
    
    def cambiar_figura(self):
        """Cambia los campos de entrada según la figura seleccionada"""
        figura = self.figura_var.get()
        
        # Limpiar resultados
        self.resultado_area.config(text="---")
        self.resultado_perimetro.config(text="---")
        
        # Limpiar canvas
        self.canvas.delete('all')
        self.canvas.create_text(160, 200, 
                               text="✏️ Escribe los valores\npara ver la figura aquí",
                               font=('Comic Sans MS', 12),
                               fill='#999', tags='ayuda')
        
        # Limpiar todos los widgets
        for widget in self.inner_entrada.winfo_children():
            widget.grid_forget()
        
        if figura == "rectangulo":
            self.label_base.grid(row=0, column=0, sticky='w', pady=8)
            self.entry_base.grid(row=0, column=1, pady=8, padx=(10, 0))
            self.entry_base.delete(0, tk.END)
            
            self.label_altura.grid(row=1, column=0, sticky='w', pady=8)
            self.entry_altura.grid(row=1, column=1, pady=8, padx=(10, 0))
            self.entry_altura.delete(0, tk.END)
            
            self.label_mensaje.config(text="🟦 ¡Perfecto! Ahora escribe la base y altura del rectángulo")
        else:
            self.label_radio.grid(row=0, column=0, sticky='w', pady=8)
            self.entry_radio.grid(row=0, column=1, pady=8, padx=(10, 0))
            self.entry_radio.delete(0, tk.END)
            
            self.label_mensaje.config(text="🔵 ¡Genial! Ahora escribe el radio del círculo")
    
    def vista_previa(self, event=None):
        """Dibuja una vista previa de la figura mientras se escribe"""
        self.canvas.delete('all')
        
        try:
            figura = self.figura_var.get()
            
            if figura == "rectangulo":
                base_str = self.entry_base.get().strip()
                altura_str = self.entry_altura.get().strip()
                
                if base_str and altura_str:
                    base = float(base_str)
                    altura = float(altura_str)
                    
                    if base > 0 and altura > 0:
                        # Escalar para que quepa en el canvas
                        max_dim = max(base, altura)
                        escala = min(250 / max_dim, 300 / max_dim)
                        
                        ancho = base * escala
                        alto = altura * escala
                        
                        x1 = 160 - ancho / 2
                        y1 = 200 - alto / 2
                        x2 = x1 + ancho
                        y2 = y1 + alto
                        
                        # Dibujar rectángulo con gradiente simulado
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                     fill='#64B5F6', 
                                                     outline='#1976D2', 
                                                     width=4)
                        
                        # Etiquetas de medidas
                        self.canvas.create_text(160, y1 - 15, 
                                               text=f"base = {base}", 
                                               font=('Comic Sans MS', 10, 'bold'),
                                               fill='#1976D2')
                        
                        self.canvas.create_text(x1 - 30, 200, 
                                               text=f"altura\n= {altura}", 
                                               font=('Comic Sans MS', 9, 'bold'),
                                               fill='#1976D2')
            else:
                radio_str = self.entry_radio.get().strip()
                
                if radio_str:
                    radio = float(radio_str)
                    
                    if radio > 0:
                        # Escalar para que quepa
                        escala = min(120 / radio, 150 / radio)
                        r = radio * escala
                        
                        self.canvas.create_oval(160 - r, 200 - r, 
                                               160 + r, 200 + r,
                                               fill='#81C784', 
                                               outline='#388E3C', 
                                               width=4)
                        
                        # Dibujar radio
                        self.canvas.create_line(160, 200, 160 + r, 200,
                                               fill='#D32F2F', width=3,
                                               arrow=tk.LAST)
                        
                        self.canvas.create_text(160 + r/2, 185, 
                                               text=f"r = {radio}", 
                                               font=('Comic Sans MS', 10, 'bold'),
                                               fill='#D32F2F')
        except:
            self.canvas.create_text(160, 200, 
                                   text="✏️ Escribe valores válidos",
                                   font=('Comic Sans MS', 12),
                                   fill='#999')
    
    def calcular(self):
        """Calcula el área y perímetro de la figura seleccionada"""
        try:
            figura = self.figura_var.get()
            
            if figura == "rectangulo":
                base_str = self.entry_base.get().strip()
                altura_str = self.entry_altura.get().strip()
                
                if not base_str or not altura_str:
                    messagebox.showwarning("⚠️ ¡Ups!", 
                                          "¡Escribe la base y la altura! 😊")
                    return
                
                base = float(base_str)
                altura = float(altura_str)
                
                rect = Rectangulo(base, altura)
                area = rect.area()
                perimetro = rect.perimetro()
                
                self.resultado_area.config(text=f"{area:.2f} u²")
                self.resultado_perimetro.config(text=f"{perimetro:.2f} u")
                
                # Actualizar puntos
                self.puntos_totales += 10
                self.calculos_realizados += 1
                self.actualizar_estadisticas()
                
                # Animar resultado
                self.animar_resultado()
                
                messagebox.showinfo("🎊 ¡Excelente!", 
                                   f"Rectángulo de {base} × {altura}\n\n"
                                   f"📊 Área: {area:.2f} unidades²\n"
                                   f"📐 Perímetro: {perimetro:.2f} unidades\n\n"
                                   f"¡Ganaste 10 puntos! ⭐")
                
                self.label_mensaje.config(text=f"🎉 ¡Perfecto! Tu rectángulo tiene {area:.2f} u² de área")
            
            else:
                radio_str = self.entry_radio.get().strip()
                
                if not radio_str:
                    messagebox.showwarning("⚠️ ¡Ups!", 
                                          "¡Escribe el radio del círculo! 😊")
                    return
                
                radio = float(radio_str)
                
                circ = Circulo(radio)
                area = circ.area()
                perimetro = circ.perimetro()
                
                self.resultado_area.config(text=f"{area:.2f} u²")
                self.resultado_perimetro.config(text=f"{perimetro:.2f} u")
                
                # Actualizar puntos
                self.puntos_totales += 10
                self.calculos_realizados += 1
                self.actualizar_estadisticas()
                
                # Animar resultado
                self.animar_resultado()
                
                messagebox.showinfo("🎊 ¡Excelente!", 
                                   f"Círculo con radio {radio}\n\n"
                                   f"📊 Área: {area:.2f} unidades²\n"
                                   f"📐 Perímetro: {perimetro:.2f} unidades\n\n"
                                   f"¡Ganaste 10 puntos! ⭐")
                
                self.label_mensaje.config(text=f"🎉 ¡Increíble! Tu círculo tiene {area:.2f} u² de área")
        
        except ValueError as e:
            if "mayores que cero" in str(e) or "mayor que cero" in str(e):
                messagebox.showerror("❌ ¡Error!", 
                                   "Los valores deben ser mayores que cero.\n\n"
                                   "Por favor usa números positivos. 😊")
            else:
                messagebox.showerror("❌ ¡Error!", 
                                   "Por favor escribe solo números.\n\n"
                                   "Ejemplo: 5 o 3.14 😊")
            self.resultado_area.config(text="---")
            self.resultado_perimetro.config(text="---")
        
        except Exception as e:
            messagebox.showerror("❌ ¡Error!", 
                               f"Algo salió mal:\n{str(e)}\n\n"
                               "¡Inténtalo de nuevo! 😊")
            self.resultado_area.config(text="---")
            self.resultado_perimetro.config(text="---")
    
    def actualizar_estadisticas(self):
        """Actualiza el contador de puntos y cálculos"""
        self.label_puntos.config(text=f"Puntos: {self.puntos_totales}")
        self.label_calculos.config(text=f"Cálculos: {self.calculos_realizados}")
        
        # Mensajes motivadores según puntos
        if self.puntos_totales >= 100:
            self.label_mensaje.config(text="🏆 ¡ERES UN MAESTRO DE LA GEOMETRÍA! 🏆")
        elif self.puntos_totales >= 50:
            self.label_mensaje.config(text="🌟 ¡Excelente progreso! ¡Sigue así!")
    
    def animar_resultado(self):
        """Anima el área de resultados"""
        colores = ['#1976D2', '#E91E63', '#4CAF50', '#FF9800']
        self.animar_color(0, colores)
    
    def animar_color(self, index, colores):
        """Cambia el color del texto varias veces"""
        if index < 6:
            color = colores[index % len(colores)]
            self.resultado_area.config(fg=color)
            self.resultado_perimetro.config(fg=color)
            self.root.after(100, lambda: self.animar_color(index + 1, colores))
        else:
            self.resultado_area.config(fg='#1976D2')
            self.resultado_perimetro.config(fg='#1976D2')
    
    def limpiar_todo(self):
        """Limpia todos los campos y resultados"""
        self.entry_base.delete(0, tk.END)
        self.entry_altura.delete(0, tk.END)
        self.entry_radio.delete(0, tk.END)
        self.resultado_area.config(text="---")
        self.resultado_perimetro.config(text="---")
        self.canvas.delete('all')
        self.canvas.create_text(160, 200, 
                               text="✏️ Escribe los valores\npara ver la figura aquí",
                               font=('Comic Sans MS', 12),
                               fill='#999', tags='ayuda')
        self.label_mensaje.config(text="🧹 ¡Todo limpio! Listo para un nuevo cálculo")


# Crear y ejecutar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = FigurasApp(ventana)
    ventana.mainloop()
