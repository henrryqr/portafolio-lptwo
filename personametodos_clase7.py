class Persona:
    def __init__(self,nombre):
        self.nombre = nombre

    def saludar(self):
        print(f"hola,soy {self.nombre}")

persona1 = Persona("maria")
persona1.saludar()
