import math

class Circulo:
    def __init__ (self, radio):
        self.radio = radio
        print("objeto circulo creado")

    def calcular_area(self):
        area = math.pi * self.radio**2
        return area

radio_usuario = float(input("Ingrese el radio del circulo: "))
circulo = Circulo(radio_usuario)
resultado = circulo.calcular_area()
print(f"El area del circulo es {resultado}")

del circulo
try:
    circulo.calcular_area()
except NameError:
    print("el objeto ya no existe")
