class Motor:
    def __init__(self,tipo):
        self.tipo = tipo

    def encender(self):
        print(f"motor: {self.tipo} encendido")

class Auto:
    def __init__(self,marca):
        self.marca = marca
        self.motor = Motor("electrico")

    def arrancar(self):
        print(f"auto: {self.marca} arrancamdo")
        self.motor.encender()
miauto=Auto("tesla")
miauto1=Auto("toyota")
miauto.arrancar()
miauto1.arrancar()

        
