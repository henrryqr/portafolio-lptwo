class Figura:
    def area(self):
        return 0


class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura


class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return (self.base * self.altura) / 2


class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        from math import pi
        return pi * self.radio * self.radio


figuras = [
    Rectangulo(4, 5),
    Triangulo(6, 2),
    Circulo(3),
    Rectangulo(10, 3)
]

for f in figuras:
    print("Área:", f.area())

