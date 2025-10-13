import gc

class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        print(f"Estudiante registrado: {self.nombre}, {self.edad} años, {self.carrera}")

    def mostrar_informacion(self):
        print(f"{self.nombre} tiene {self.edad} años y estudia {self.carrera}")

    def __del__(self):
        print(f"Estudiante eliminado: {self.nombre}")


n = int(input("¿Cuántos estudiantes deseas registrar? "))

datos_estudiante = []
for i in range(n):
    print(f"\n--- Registro del estudiante {i+1} ---")
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    carrera = input("Carrera: ")
    estudiante = Estudiante(nombre, edad, carrera)
    datos_estudiante.append(estudiante)


grupo = []
for estudiante in datos_estudiante:
    estudiante.mostrar_informacion()
    grupo.append(estudiante)


grupo.clear()
del estudiante
gc.collect()

print("\nFin del programa")
