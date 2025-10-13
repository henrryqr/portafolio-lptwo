class Temperatura:
    def __init__(self):
        self.__fahrenheit = 0
        
    def get_fahrenheit(self):
        return self.__fahrenheit
    
    def set_fahrenheit(self, valor):
        self.__fahrenheit = valor
    
    def fahrenheit_a_celsius(self):
        return (self.__fahrenheit - 32) * 5/9

    
temp = Temperatura()

f = float(input("Ingresa temperatura en °F: "))
temp.set_fahrenheit(f)
print(f"{f}°F = {temp.fahrenheit_a_celsius():.2f}°C")
