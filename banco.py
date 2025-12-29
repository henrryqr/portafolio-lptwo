class CuentaBancaria:
    def __init__(self, titular, saldo=100):
        self.titular = titular
        self.saldo = saldo
        print(f"Bienvenido {self.titular}, cuenta creada con saldo {self.saldo}.")

    def depositar(self, monto):
        self.saldo += monto
        print(f"depósito de {monto} realizado. Saldo actual: {self.saldo}")

    def retirar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto
            print(f"retiro de {monto} realizado. Saldo actual: {self.saldo}")
        else:
            print("fondos insuficientes.")

    def __del__(self):
        print(f"cuenta de {self.titular} cerrada.")

titular = input("ingrese el nombre del titular: ")
saldo_inicial = float(input("ingrese el saldo inicial: "))

cuenta1 = CuentaBancaria(titular, saldo_inicial)

deposito = float(input("ingrese el monto a depositar: "))
cuenta1.depositar(deposito)

retiro = float(input("ingrese el monto a retirar: "))
cuenta1.retirar(retiro)

del cuenta1

try:
    print(cuenta1)
except NameError:
    print("la cunta ya no existe")
