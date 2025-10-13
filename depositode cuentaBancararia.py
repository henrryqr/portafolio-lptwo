class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo
        print(f" Bienvenido a objeto a sido creado Cuenta de {self.titular}  {self.saldo} soles.")

    def depositar(self, monto):
        self.saldo += monto
        print(f"Se depositaron {monto} soles. Saldo actual: {self.saldo} soles.")

    def retirar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto
            print(f"Se retiraron {monto} soles. Saldo actual: {self.saldo} soles.")
        else:
            print(f"No hay fondos suficientes para retirar {monto} soles.")

    def __del__(self):
        print(f"Cuenta de {self.titular} cerrada.")


cuenta = CuentaBancaria("Luis Quenaya Loza", 500)

cuenta.depositar(100)
cuenta.retirar(200)
cuenta.retirar(50)  

del cuenta

try:
    cuenta.depositar(100)
except NameError:
    print("La cuenta ya ha sido eliminada.")

        
