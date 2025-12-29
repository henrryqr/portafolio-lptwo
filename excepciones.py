class DivisionPorCeroError(Exception):
    pass


class CalculadoraSegura:
    def dividir(self, a, b):
        if b == 0:
            raise DivisionPorCeroError("Division por cero")
        return a / b


c = CalculadoraSegura()

pares = [(10, 2), (5, 0), (9, 3)]

for a, b in pares:
    try:
        print("Resultado:", c.dividir(a, b))
    except DivisionPorCeroError as e:
        print("Error:", e)
