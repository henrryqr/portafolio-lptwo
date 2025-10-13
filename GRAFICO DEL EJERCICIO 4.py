import tkinter as tk
from tkinter import messagebox

class Ladrillo:
    def __init__(self, longitud, altura, ancho):
        self.longitud = longitud
        self.altura = altura
        self.ancho = ancho

    def calcular_cantidad(self):
        return 1 / ((self.longitud + 0.015) * (self.altura + 0.015))

def calcular():
    try:
        longitud = float(entry_longitud.get())
        altura = float(entry_altura.get())
        ancho = float(entry_ancho.get())

        mi_ladrillo = Ladrillo(longitud, altura, ancho)

        cantidad = mi_ladrillo.calcular_cantidad()
        area_con_desperdicio = cantidad * 1.05
        area_pared = area_con_desperdicio * 8.05

        resultado.set(
            f"Cantidad de ladrillos/m² (sin desperdicio): {cantidad:.2f}\n"
            f"Área del rectángulo (con desperdicio): {area_con_desperdicio:.2f}\n"
            f"Área total (con área de la pared): {area_pared:.2f}"
        )
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Cálculo de Ladrillos")
ventana.geometry("400x300")
ventana.resizable(False, False)

# Etiquetas y entradas
tk.Label(ventana, text="Longitud (m):").pack()
entry_longitud = tk.Entry(ventana)
entry_longitud.pack()

tk.Label(ventana, text="Altura (m):").pack()
entry_altura = tk.Entry(ventana)
entry_altura.pack()

tk.Label(ventana, text="Ancho (m):").pack()
entry_ancho = tk.Entry(ventana)
entry_ancho.pack()

# Botón de cálculo
tk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)

# Resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, justify="left", fg="blue").pack()

ventana.mainloop()
