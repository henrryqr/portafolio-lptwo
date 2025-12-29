# -----------------------------------
# CLASE BASE
# -----------------------------------
class Pago:
    def __init__(self, monto):
        self.monto = monto

    def realizar_pago(self):
        print(f"Procesando pago de S/.{self.monto:.2f}")


# -----------------------------------
# SUBCLASES (SIN usar super)
# -----------------------------------
class TarjetaCredito(Pago):
    def __init__(self, monto, numero_tarjeta):
        self.monto = monto
        self.numero_tarjeta = numero_tarjeta

    def realizar_pago(self):
        print(f"💳 Pago de S/.{self.monto:.2f} con tarjeta N° {self.numero_tarjeta[-4:]} realizado correctamente.")


class PayPal(Pago):
    def __init__(self, monto, correo):
        self.monto = monto
        self.correo = correo

    def realizar_pago(self):
        print(f"🌐 Pago de S/.{self.monto:.2f} mediante PayPal ({self.correo}) realizado correctamente.")


class Efectivo(Pago):
    def __init__(self, monto):
        self.monto = monto

    def realizar_pago(self):
        print(f"💵 Pago en efectivo de S/.{self.monto:.2f} realizado correctamente.")


class Yape(Pago):
    def __init__(self, monto, numero):
        self.monto = monto
        self.numero = numero

    def realizar_pago(self):
        print(f"📱 Pago de S/.{self.monto:.2f} realizado con Yape al número {self.numero}.")


class Plin(Pago):
    def __init__(self, monto, numero):
        self.monto = monto
        self.numero = numero

    def realizar_pago(self):
        print(f"📲 Pago de S/.{self.monto:.2f} realizado con Plin al número {self.numero}.")


# -----------------------------------
# MENÚ INTERACTIVO (POLIMORFISMO)
# -----------------------------------
def menu_pago():
    print("\n=== SISTEMA DE PAGOS ===")
    print("1. Tarjeta de Crédito")
    print("2. PayPal")
    print("3. Efectivo")
    print("4. Yape")
    print("5. Plin")
    print("========================")

    opcion = input("Seleccione método de pago (1-5): ")
    monto = float(input("Ingrese monto del pago: S/."))

    if opcion == "1":
        num = input("Ingrese número de tarjeta: ")
        pago = TarjetaCredito(monto, num)
    elif opcion == "2":
        correo = input("Ingrese correo de PayPal: ")
        pago = PayPal(monto, correo)
    elif opcion == "3":
        pago = Efectivo(monto)
    elif opcion == "4":
        num = input("Ingrese número de Yape: ")
        pago = Yape(monto, num)
    elif opcion == "5":
        num = input("Ingrese número de Plin: ")
        pago = Plin(monto, num)
    else:
        print("❌ Opción no válida.")
        return

    # Polimorfismo: mismo método, distinto comportamiento
    pago.realizar_pago()


# -----------------------------------
# PROGRAMA PRINCIPAL
# -----------------------------------
if __name__ == "__main__":
    while True:
        menu_pago()
        continuar = input("\n¿Desea realizar otro pago? (s/n): ").lower()
        if continuar != "s":
            print("👋 Gracias por usar el sistema de pagos.")
            break

    metodo.pagar(monto)
