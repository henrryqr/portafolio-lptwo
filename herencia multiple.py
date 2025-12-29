class Vehiculo:
    def acelerar(self):
        return "El vehículo está acelerando"


class Volador:
    def volar(self):
        return "El objeto está volando"


class Avion(Vehiculo, Volador):
    def __init__(self, modelo):
        self.modelo = modelo
        self.en_aire = False

    def despegar(self):
        self.en_aire = True
        return "El avión ha despegado"


av = Avion("Boeing 747")
print("Modelo:", av.modelo)
print(av.acelerar())
print(av.despegar())
print(av.volar() if av.en_aire else "No puede volar aún")
