class CursoLenguajeProgramacionII:
    def __init__(self, nombre, codigo, profesor):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        print(">>> Objeto del curso creado correctamente")

    def mostrar_informacion(self):
        print("\n===== Información del Curso =====")
        print(f"Nombre del curso : {self.nombre}")
        print(f"Código del curso : {self.codigo}")
        print(f"Profesor         : {self.profesor}")

    def __del__(self):
        print(f">>> El curso '{self.nombre}' ha sido eliminado.")


def main():
    cursos = []
    n = int(input("¿Cuántos cursos deseas registrar?: "))

    for i in range(n):
        print(f"\n--- Curso {i + 1} ---")
        nombre = input("Ingrese el nombre del curso: ")
        codigo = input("Ingrese el código del curso: ")
        profesor = input("Ingrese el nombre del profesor: ")
        curso = CursoLenguajeProgramacionII(nombre, codigo, profesor)
        cursos.append(curso)

    print("\n=== LISTA DE CURSOS REGISTRADOS ===")
    for curso in cursos:
        curso.mostrar_informacion()

    eliminar = input("\n¿Deseas eliminar todos los cursos? (s/n): ").lower()
    if eliminar == "s":
        for curso in cursos:
            del curso
        cursos.clear()
        print("\n>>> Todos los cursos han sido eliminados.")


if __name__ == "__main__":
    main()
