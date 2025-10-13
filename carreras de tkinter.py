import tkinter as tk
from tkinter import messagebox
import gc

class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        print(f"Estudiante registrado: {self.nombre}, {self.edad} años, {self.carrera}")

    def mostrar_informacion(self):
        return f"{self.nombre} tiene {self.edad} años y estudia {self.carrera}"

    def __del__(self):
        print(f"Estudiante eliminado: {self.nombre}")


# Lista para guardar estudiantes
datos_estudiante = []

# ---- Funciones de Tkinter ----
def registrar_estudiante():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    carrera = entry_carrera.get()

    if not nombre or not edad or not carrera:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return
    
    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número")
        return

    estudiante = Estudiante(nombre, edad, carrera)
    datos_estudiante.append(estudiante)

    lista_estudiantes.insert(tk.END, estudiante.mostrar_informacion())
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_carrera.delete(0, tk.END)


def eliminar_estudiantes():
    datos_estudiante.clear()
    lista_estudiantes.delete(0, tk.END)
    gc.collect()
    messagebox.showinfo("Información", "Todos los estudiantes fueron eliminados")


# ---- Interfaz ----
root = tk.Tk()
root.title("Registro de Estudiantes")

# Etiquetas y entradas
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Edad:").grid(row=1, column=0, padx=5, pady=5)
entry_edad = tk.Entry(root)
entry_edad.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Carrera:").grid(row=2, column=0, padx=5, pady=5)
entry_carrera = tk.Entry(root)
entry_carrera.grid(row=2, column=1, padx=5, pady=5)

# Botones
btn_registrar = tk.Button(root, text="Registrar", command=registrar_estudiante)
btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

btn_eliminar = tk.Button(root, text="Eliminar todos", command=eliminar_estudiantes)
btn_eliminar.grid(row=4, column=0, columnspan=2, pady=5)

# Lista de estudiantes
lista_estudiantes = tk.Listbox(root, width=50)
lista_estudiantes.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
