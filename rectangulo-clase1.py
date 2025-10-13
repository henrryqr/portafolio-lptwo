class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

# Crear un objeto de la clase Rectangulo
operacion = Rectangulo(5, 6)

print("El área del rectángulo es:", operacion.calcular_area())
