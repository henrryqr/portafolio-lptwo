class departamento:
    def __init__(self, nombre):
        self.nombre = nombre

class universidad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.departamento = []

    def agregar_departamento(self, departamento):
        self.departamento.append(departamento)

dep1 = departamento("ingeniería estadística")
dep2 = departamento("informática")

uni = universidad("UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO")
uni.agregar_departamento(dep1)
uni.agregar_departamento(dep2)

print(f"Departamentos de {uni.nombre}:")
print("- " + uni.departamento[0].nombre)
print("- " + uni.departamento[1].nombre)
