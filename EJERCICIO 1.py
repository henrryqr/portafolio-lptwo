
class Persona:
    def __init__(self, peso, altura):
        self.peso = peso
        self.altura = altura
    
    def calcular_imc(self):
        imc = self.peso / (self.altura ** 2)
        return imc
    
    def clasificar_imc(self):
        imc = self.calcular_imc()
        if imc < 18.5:
            return "Bajo peso"
        elif 18.5 <= imc <= 24.9:
            return "Normal"
        elif 25.0 <= imc <= 29.9:
            return "Sobrepeso"
        elif 30.0 <= imc <= 34.9:
            return "Obesidad grado I"
        elif 35.0 <= imc <= 39.9:
            return "Obesidad grado II"
        else:
            return "Obesidad grado III (mórbida)"

peso = float(input("Ingresa tu peso en kg: "))
altura = float(input("Ingresa tu altura en metros: "))

persona = Persona(peso, altura)

print(f"Tu IMC es: {persona.calcular_imc():.2f}")
print(f"Clasificación: {persona.clasificar_imc()}")
