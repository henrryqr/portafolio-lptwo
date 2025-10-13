class NumeroMultiplo:
    def __init__(self, valor):
        self.valor = valor

    def mostrar_multiplo(self):
        if self.valor == 0:
            print(f"El: {self.valor} es número nulo")
        elif self.valor % 3 == 0 and self.valor % 5 == 0:
            print(f"Número: : {self.valor} es múltiplo de 3 y de 5")
        elif self.valor % 3 == 0:
            print(f"Número: : {self.valor} es múltiplo de 3")
        elif self.valor % 5 == 0:
            print(f"Número: : {self.valor} es múltiplo de 5")
        else:
            print(f"Número: : {self.valor} No es múltiplo de 3 ni de 5")
        
        print("-"*60)

def main():
    i = 0
    while i <= 10:
        numero = NumeroMultiplo(i)
        numero.mostrar_multiplo()
        i += 1

if __name__ == "__main__":
    
    main()
