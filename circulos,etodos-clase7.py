import math
class Circulo:
    def __init__(self,radio):
        self.radio = radio

    def calcular_area(self):
        area = math.pi * self.radio**2
        return area
    def calcular_perimetro(self):
        perimetro = 2*math.pi*self,radio
        return perimetro
    def mostrar_informacion(self):
        print (f"radio del circulo es; {self.radio}")
        print (f"perimetro del circulo es; {self.calcular_area()}")
        print (f"el perimetro es ; {self.calcular_perimetro}")

circulo = Circulo(7)
circulo.mostrar_informacion()
