class Motor:
    def __init__(self, potencia):
        self.potencia = potencia
        self.encendido = False

    def encender(self):
        self.encendido = True
        return "Motor encendido"


class Auto:
    def __init__(self, marca, motor):
        self.marca = marca
        self.motor = motor

    def arrancar(self):
        if self.motor.encendido:
            return "El auto ya estaba encendido"
        return self.motor.encender() + " | Auto arrancó"


m = Motor(180)
a = Auto("Hyundai", m)

print(a.arrancar())
print(a.arrancar())
