class Temperatura:
    def __init__(self, celsius=0):
        self.__celsius = celsius   


    def get_celsius(self):
        return self.__celsius
    
    def set_celsius(self, valor):
        self.__celsius = valor
    

    def celsius_a_fahrenheit(self):
        return (self.__celsius * 9/5) + 32

    
temp = Temperatura()

c = float(input("Ingresa temperatura en °C: "))
temp.set_celsius(c)
print(f"{c}°C = {temp.celsius_a_fahrenheit():.2f}°F")
