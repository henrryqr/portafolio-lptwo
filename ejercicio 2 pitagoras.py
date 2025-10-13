class Pitagoras:
    def __init__(self, catetoa, catetob):
        self.catetoa = catetoa
        self.catetob = catetob
        
    def calcular_hipotenusa(self):
        return (self.catetoa**2 + self.catetob**2)**0.5



catetoa = int(input("Ingrese el valor de cateto A: "))
catetob = int(input("Ingrese el valor de cateto B: "))


mi_hipotenusa = Pitagoras(catetoa, catetob)


print(f"La hipotenusa es: {mi_hipotenusa.calcular_hipotenusa()}")
