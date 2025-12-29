class Operacion:
    def calcular(self, a, b):
        raise NotImplementedError("debe implementar el metodo calcular")
class Suma(Operacion):
    def calcular(self, a, b):
        return a + b
class Resta(Operacion):
    def calcular(self, a, b):
        return a - b
class Multiplicacion(Operacion):
    def calcular(self, a, b):
        return a * b
class Division(Operacion):
    def calcular(self, a, b):
        if b == 0:
            raise ValueError("no se puede dividir entre cero")
        return a / b
class Calculadora:
    def __init__(self, operacion: Operacion):
        self.operacion = operacion
    def ejecutar(self, a, b):
        return self.operacion.calcular(a, b)

a = 9
b = 3

calc_suma = Calculadora(Suma())
print("Suma:", calc_suma.ejecutar(a, b))

calc_resta = Calculadora(Resta())
print("Resta:", calc_resta.ejecutar(a, b))

calc_mult = Calculadora(Multiplicacion())
print("Multiplicación:", calc_mult.ejecutar(a, b))

calc_div = Calculadora(Division())
print("División:", calc_div.ejecutar(a, b))
