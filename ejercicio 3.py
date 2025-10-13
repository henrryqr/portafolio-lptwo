
              
class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura
    def calcular_perimetro(self):
        return self.base * self.altura

mi_rectangulo = Rectangulo(5, 6)


print(f"El área es: ",{mi_rectangulo.calcular_area()})
print(f"El perimetro es: ",{mi_rectangulo.calcular_perimetro()})
