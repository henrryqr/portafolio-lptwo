class profesor:
    def __init__(self, nombre):
        self.nombre = nombre

class curso:
    def __init__(self, nombre, profesor):
        self.nombre = nombre
        self.profesor = profesor  # Aquí se guarda el objeto profesor

prof = profesor("Dr.Murillo")
curso = curso("muestreo", prof)
print(curso.profesor.nombre)
