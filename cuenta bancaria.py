class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = float(saldo)

    def depositar(self, cant):
        if cant > 0:
            self.saldo = self.saldo + cant

    def retirar(self, monto):
        if monto > 0 and monto <= self.saldo:
            self.saldo = self.saldo - monto
            return True
        print("No se puede retirar")
        return False

    def mostrar_saldo(self):
        return "Titular:" + self.titular + " | Saldo:" + str(self.saldo)


c1 = CuentaBancaria("Ana", 150)
c2 = CuentaBancaria("Luis", 80)

c1.depositar(20)
c2.retirar(30)
c2.retirar(100)

print(c1.mostrar_saldo())
print(c2.mostrar_saldo())
