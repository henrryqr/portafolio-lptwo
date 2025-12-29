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
                raise ZeroDivisionError("No se puede dividir entre cero")
            return self.a / self.b
        except Exception as e:
            raise TypeError(f"Error al dividir: {e}")


# ============================
#   INTERFAZ TKINTER
# ============================

def ejecutar_operacion(operacion):
    try:
        tipo = tipo_dato.get()

        if tipo == "int":
            a = int(entry_a.get())
            b = int(entry_b.get())
            calc = Calculadora[int](a, b)
        else:
            a = float(entry_a.get())
            b = float(entry_b.get())
            calc = Calculadora[float](a, b)

        if operacion == "sumar":
            resultado = calc.sumar()
        elif operacion == "restar":
            resultado = calc.restar()
        elif operacion == "multiplicar":
            resultado = calc.multiplicar()
        elif operacion == "dividir":
            resultado = calc.dividir()

        messagebox.showinfo("Resultado", f"Resultado: {resultado}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ============================
#   VENTANA PRINCIPAL
# ============================

ventana = tk.Tk()
ventana.title("Calculadora Genérica Tkinter")
ventana.geometry("300x300")

tk.Label(ventana, text="Valor A:").pack()
entry_a = tk.Entry(ventana)
entry_a.pack()

tk.Label(ventana, text="Valor B:").pack()
entry_b = tk.Entry(ventana)
entry_b.pack()

tk.Label(ventana, text="Tipo de dato:").pack()
tipo_dato = ttk.Combobox(ventana, values=["int", "float"])
tipo_dato.current(0)
tipo_dato.pack()

# Botones de operaciones
tk.Button(ventana, text="Sumar", command=lambda: ejecutar_operacion("sumar")).pack(pady=5)
tk.Button(ventana, text="Restar", command=lambda: ejecutar_operacion("restar")).pack(pady=5)
tk.Button(ventana, text="Multiplicar", command=lambda: ejecutar_operacion("multiplicar")).pack(pady=5)
tk.Button(ventana, text="Dividir", command=lambda: ejecutar_operacion("dividir")).pack(pady=5)

ventana.mainloop()
