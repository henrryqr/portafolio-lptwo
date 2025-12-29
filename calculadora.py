from typing import TypeVar, Generic

T = TypeVar('T', int, float)

class Calculadora(Generic[T]):
    def __init__(self, a: T, b: T):
        self.a = a
        self.b = b

    def sumar(self) -> T:
        return self.a + self.b   

    def restar(self) -> T:
        return self.a - self.b

    def multiplicar(self) -> T:  
        return self.a * self.b

    def dividir(self) -> T:
        if self.b == 0:          
            raise ValueError("No se puede dividir entre cero")
        return self.a / self.b



cal_int = Calculadora[int](10, 2)
print("Suma: ", cal_int.sumar())
print("Resta: ", cal_int.restar())
print("Multiplicación: ", cal_int.multiplicar())
print("División: ", cal_int.dividir())

cal_float = Calculadora [float] (8.4,3.4)
print("Suma: ", cal_int.sumar())
print("Resta: ", cal_int.restar())
print("Multiplicación: ", cal_int.multiplicar())
print("División: ", cal_int.dividir())



