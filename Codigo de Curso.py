import gc

class Curso:
    def __init__(self, nombre, codigo, profesor):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        print(f"Curso registrado: {self.nombre}, Código: {self.codigo}, Profesor: {self.profesor}")

    def mostrar_informacion(self):
        print(f"Curso: {self.nombre} | Código: {self.codigo} | Profesor: {self.profesor}")

    def __del__(self):
        print(f"Curso eliminado: {self.nombre}")


cursos_datos = [
    ("Lenguaje de Programación 2", "EST 305", "Coyla Idme Leonel"),
    ("Base de Datos", "EST 310", "Perez Quispe Ana")
]

inventario = []
for datos in cursos_datos:
    curso = Curso(*datos)         
    curso.mostrar_informacion()
    inventario.append(curso)

inventario.clear()
del curso
gc.collect()

print("\nFin del programa")

