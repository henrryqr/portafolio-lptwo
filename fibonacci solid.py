# Principio S (Single Responsibility)
class CalculadoraFibonacci:
    def calcular(self):
        raise NotImplementedError("Debe implementar el método calcular")


# Principio O y L (Open/Closed y Liskov Substitution)
class FibonacciIterativo(CalculadoraFibonacci):
    def __init__(self, numero):
        self.numero = numero

    def calcular(self):
        serie = [0, 1]
        for i in range(2, self.numero):
            serie.append(serie[-1] + serie[-2])
        return serie[:self.numero]


# Principio D (Dependency Inversion)
class ClienteFibonacci:
    def __init__(self, calculadora: CalculadoraFibonacci):
        self.calculadora = calculadora

    def ejecutar(self):
        resultado = self.calculadora.calcular()
        print(f"Serie de Fibonacci: {resultado}")


# Uso con implementación iterativa
fibonacci_iter = FibonacciIterativo(10)
cliente_iter = ClienteFibonacci(fibonacci_iter)
cliente_iter.ejecutar()

