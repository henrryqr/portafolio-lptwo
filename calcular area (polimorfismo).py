class Figura:
    def calcular_area(self):
        pass

class Cuadrado(Figura):
    def __init__(self):
        self.lado = 4  

    def calcular_area(self):
        return self.lado * self.lado

class Triangulo(Figura):
    def __init__(self):
        self.base = 6
        self.altura = 3

    def calcular_area(self):
        return (self.base * self.altura) / 2

class Circulo(Figura):
    def __init__(self):
        self.radio = 5

    def calcular_area(self):
        from math import pi
        return pi * self.radio ** 2

figuras = [Cuadrado(), Triangulo(), Circulo()]

for figura in figuras:
    print(f"{figura.__class__.__name__}: Área = {figura.calcular_area():.2f}")
