import math

class Hipotenusa:
    def __init__(self, catetoa, catetob):
        self.catetoa = catetoa
        self.catetob = catetob

    def calcular_hipotenusa(self):
        hipotenusa = math.sqrt(self.catetoa**2 + self.catetob**2)
        return hipotenusa

    def mostrar_informacion(self):
        print(f"Cateto a: {self.catetoa}")
        print(f"Cateto b: {self.catetob}")
        print(f"Hipotenusa del triángulo es: {self.calcular_hipotenusa()}")


# Uso de la clase
triangulo = Hipotenusa(3, 4)
triangulo.mostrar_informacion()
