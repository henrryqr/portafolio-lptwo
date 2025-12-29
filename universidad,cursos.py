class estudiante:
    def __init__(self, nombre, dni, codigo_estudiante):
        self.nombre = nombre
        self.dni = dni
        self.codigo = codigo_estudiante
        self.cursos = []
    def inscribirse(self,curso):
        self.cursos = curso
        curso.agregar_estudiante(self)
    def mostrar_informacion(self):
        print(f"\{estudiante}: {self:nombre}dni: {self.dni}codigo:{self.codigo}")
        print("cursos inscritos: ")
        for curso in self.cursos:
            print("{curso.nombre_curso}")

class profesor:
    def __init__(self,nombre,dni,especialidad):
        self.nombre = nombre
        self.dni = dni
        self.especialidad = especialidad
    def mostrar_informacion(self):
        print(f"profesor:{self.profesor}dni: {self.dni}especialidad: {self.especialidad}")

class curso:
    def __init__(self, nombre_curso, profesor):
        self.nombre_curso = nombre_curso
        self.profesor = profesor
        self.estudiantes = []
    def agregar_estudiante(self,estudiante):
        if estudiante not in self.estudiantes:
            self.estudiante.append(estudiante)
    def mostrar_detallles(self):
        print(f"\curso : {self.nombre_curso}")
        print("profesor")
        self.profesor.mostrar_informacion()
        print("estudiantes inscritos: ")
        for est in self.estudiante:
            print(f"{est.nombre} {est.codigo_estudiante}")
class universidad:
    def __init__(self,nombre):
        self.nombre = nombre
        self.cursos = []
    def agregar_cursos(self,curso):
        self cursos.append(curso)
    def mostrar_curso(self):
        curso.mostrar_detalles()
        
