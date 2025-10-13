class NumeroMultiplo:
    def __init__(self, valor):   # 👈 dos guiones bajos
        self.valor = valor

    def mostrar_multiplo(self):
        if self.valor == 0:
            print(f"El número {self.valor} es número nulo")
        elif self.valor % 3 == 0 and self.valor % 5 == 0:
            print(f"El número {self.valor} es múltiplo de 3 y de 5")
        elif self.valor % 3 == 0:
            print(f"El número {self.valor} es múltiplo de 3")
        elif self.valor % 5 == 0:
            print(f"El número {self.valor} es múltiplo de 5")
        else:
            print(f"El número {self.valor} no es múltiplo de 3 ni de 5")

def main():
    print("-" * 60)
    i = 0
    while i <= 10:
        numero = NumeroMultiplo(i)
        numero.mostrar_multiplo()
        i += 1

if __name__ == "__main__":   # 👈 doble guion bajo
    main()

