class Fibonacci:
    def __init__(self, cantidad):
        self.cantidad = cantidad
        self.serie = []

    def generarSerie(self):
        a, b = 0, 1
        for _ in range(self.cantidad):
            self.serie.append(a)
            a, b = b, a + b
        return self.serie


def main():
    cantidad = int (input("Ingrese la cantidad de la serie"))
    miFibonacci = Fibonacci(cantidad)
    resultado = miFibonacci.generarSerie()
    print(resultado)


if __name__ == "__main__":
    main()
