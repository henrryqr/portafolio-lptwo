import tkinter as tk
from tkinter import messagebox

def identificar_funcion():
    expr = entrada.get().replace(" ", "")  # Quitamos espacios
    tipo = "Desconocida"
    
    # Verificamos si es lineal (contiene x y no x**2 ni x**3)
    if "x**3" in expr:
        tipo = "Cúbica"
    elif "x**2" in expr:
        tipo = "Cuadrática"
    elif "exp" in expr:
        tipo = "Exponencial"
    elif "x" in expr:
        tipo = "Lineal"
    
    messagebox.showinfo("Resultado", f"La función ingresada es: {tipo}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Identificador de Funciones")
ventana.geometry("400x150")

# Widgets
tk.Label(ventana, text="Ingrese una función de x:").pack(pady=10)
entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=5)

boton = tk.Button(ventana, text="Identificar función", command=identificar_funcion)
boton.pack(pady=10)

ventana.mainloop()
