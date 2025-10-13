class Estudiante:
    def __init__(self, nombre, dni, codigo_estudiante):
        self.nombre = nombre
        self.dni = dni
        self.codigo = codigo_estudiante
        self.cursos = []  # lista de cursos inscritos

    def inscribirse(self, curso):
        if curso not in self.cursos:
            self.cursos.append(curso)
            curso.agregar_estudiante(self)  # registrar también al estudiante en el curso

    def mostrar_informacion(self):
        print(f"\nEstudiante: {self.nombre}  DNI: {self.dni}  Código: {self.codigo}")
        print("Cursos inscritos:")
        if not self.cursos:
            print("  (No tiene cursos inscritos)")
        else:
            for curso in self.cursos:
                print(f"  - {curso.nombre_curso}")


class Profesor:
    def __init__(self, nombre, dni, especialidad):
        self.nombre = nombre
        self.dni = dni
        self.especialidad = especialidad

    def mostrar_informacion(self):
        print(f"Profesor: {self.nombre}  DNI: {self.dni}  Especialidad: {self.especialidad}")


class Curso:
    def __init__(self, nombre_curso, profesor):
        self.nombre_curso = nombre_curso
        self.profesor = profesor
        self.estudiantes = []

    def agregar_estudiante(self, estudiante):
        if estudiante not in self.estudiantes:
            self.estudiantes.append(estudiante)

    def mostrar_detalles(self):
        print(f"\nCurso: {self.nombre_curso}")
        print("Profesor:")
        self.profesor.mostrar_informacion()
        print("Estudiantes inscritos:")
        if not self.estudiantes:
            print("  (No hay estudiantes inscritos)")
        else:
            for est in self.estudiantes:
                print(f"  - {est.nombre} ({est.codigo})")


class Universidad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cursos = []

    def agregar_curso(self, curso):  # nombre del parámetro corregido
        self.cursos.append(curso)

    def mostrar_cursos(self):
        print(f"\nUniversidad: {self.nombre}")
        for curso in self.cursos:
            curso.mostrar_detalles()


# --- Creación de objetos ---
prof1 = Profesor("Ing. Juan Carlos", "0132301", "Programación")
prof2 = Profesor("ing. fred","02154689","estadistica")
prof3 = Profesor("ing. milan","89653214","estadistica")

curso1 = Curso("Lenguaje de Programación II", prof1)
curso2 = Curso("Estructura de Datos", prof2)
curso3 = Curso("inferencia estadistica",prof3)

est1 = Estudiante("Milena Kely", "12345678", 201546)
est2 = Estudiante("Henry Quispe", "156489521", 240598)

univ = Universidad("Universidad Nacional del Altiplano")
univ.agregar_curso(curso1)
univ.agregar_curso(curso2)

est1.inscribirse(curso1)
est1.inscribirse(curso2)
est2.inscribirse(curso2)

# --- Mostrar información ---
univ.mostrar_cursos()
est1.mostrar_informacion()
est2.mostrar_informacion()

prof2.mostrar_informacion()
prof3.mostrar_informacion()
