class CalculadoraSuma:
    def __init__(self):
        self.total = 0

    def sumarNumeros(self):
        print("Calcula la suma de números ingresados.")
        print("Escribe números para sumar. Escribe 'fin' para terminar.")
        entrada = ""
        while entrada.lower() != "fin":
            entrada = input("Ingrese un número: ")

            if entrada.isdigit():
                self.total += int(entrada)
                    print(f"El {self.total} es un número NULO")
                elif self.total % 2 == 0:
                    print(f"El {self.total} es un número PAR")
                else:
                    print(f"El {self.total} es un número IMPAR")
            elif entrada.lower() != "fin":
                print("Entrada inválida: Escribe un número o 'fin' ")
            
            print("-" * 30) 

        print(f"La suma total es: {self.total}")

def main():
    calculadora = CalculadoraSuma()
    calculadora.sumarNumeros()

if __name__ == "__main__":
    main()
