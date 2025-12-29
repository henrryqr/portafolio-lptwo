class FiguraGeometrica:
    def area(self):
        raise NotImplementedError("Debe implementar el método area")

    def perimetro(self):
        raise NotImplementedError("Debe implementar el método perimetro")


class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.1415 * (self.radio ** 2)

    def perimetro(self):
        return 2 * 3.1415 * self.radio


class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


class Figura:
    def __init__(self, figura: FiguraGeometrica):
        self.figura = figura

    def ejecutar(self):
        print(f"Área: {self.figura.area()}")
        print(f"Perímetro: {self.figura.perimetro()}")


circulo = Circulo(4)
figura_circulo = Figura(circulo)
figura_circulo.ejecutar()

rectangulo = Rectangulo(3, 4)
figura_rectangulo = Figura(rectangulo)
figura_rectangulo.ejecutar()
