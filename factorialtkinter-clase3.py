
import tkinter as tk
from tkinter import messagebox

# Clase factorial
class Factorial:
    def __init__(self, numero):
        self.numero = numero
        self.resultado = 1

    def calcular(self):
        if self.numero < 0:
            return None
        for i in range(1, self.numero + 1):
            self.resultado *= i
        return self.resultado

# Función para manejar el evento del botón
def calcular_factorial():
    try:
        numero = int(entry_numero.get())
        mifactorial = Factorial(numero)
        resultado = mifactorial.calcular()
        if resultado is None:
            messagebox.showerror("Error", "El factorial no está definido para números negativos.")
        else:
            label_resultado.config(text=f"El factorial de {numero} es:\n{resultado}")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un número entero válido.")

# Ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Factorial")
ventana.geometry("350x250")
ventana.config(bg="#E8F0FE")

# Etiquetas
label_titulo = tk.Label(ventana, text="Calculadora de Factorial", font=("Arial", 14, "bold"), bg="#E8F0FE")
label_titulo.pack(pady=10)

label_ingreso = tk.Label(ventana, text="Ingrese un número:", font=("Arial", 11), bg="#E8F0FE")
label_ingreso.pack()

# Entrada
entry_numero = tk.Entry(ventana, font=("Arial", 11), justify="center")
entry_numero.pack(pady=5)

# Botón
boton_calcular = tk.Button(ventana, text="Calcular", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                           command=calcular_factorial)
boton_calcular.pack(pady=10)

# Etiqueta de resultado
label_resultado = tk.Label(ventana, text="", font=("Arial", 11, "bold"), fg="blue", bg="#E8F0FE", wraplength=300)
label_resultado.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()

