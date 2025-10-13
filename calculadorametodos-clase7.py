class Calculadora:
    def sumar(self,a,b):
        self.a=a
        self.b =b
        return self.a + self.b

calculadora = Calculadora()
suma = calculadora.sumar(6,5)

print(f"La suma de {calculadora.a} y {calculadora.b} es:", suma)
