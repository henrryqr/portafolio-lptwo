class Factorial:
    def __init__ (self, numero):
        self.numero = numero
        self.resultado = 1
        
    def calcular (self):
        if self.numero < 0:
            print ("El factorial no esta definido para numeros negativios")
            return None
        
        for i in range(1,self.numero+1):
            self.resultado *= i
        return self.resultado
def main():
    miFactorial = Factorial(5)
    resultado = miFactorial.calcular()
    if resultado is not None:
        print (f"El factorial de (miFactorial.numero) es (resultado)")
if __name__=="__main__":
    main()
