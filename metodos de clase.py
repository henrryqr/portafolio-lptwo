class ConversorTemperatura:
    def __init__(self, f):
        self.fahrenheit = f

    def metodo_desde_celsius(cls, c):
        f = cls.metodo_celsius_a_fahrenheit(c)
        return cls(f)

    def metodo_celsius_a_fahrenheit(c):
        return (c * 9 / 5) + 32


ConversorTemperatura.desde_celsius = classmethod(ConversorTemperatura.metodo_desde_celsius)
ConversorTemperatura.celsius_a_fahrenheit = staticmethod(ConversorTemperatura.metodo_celsius_a_fahrenheit)

t1 = ConversorTemperatura.desde_celsius(0)
t2 = ConversorTemperatura.desde_celsius(25)
t3 = ConversorTemperatura(212)

print(t1.fahrenheit)
print(t2.fahrenheit)
print(ConversorTemperatura.celsius_a_fahrenheit(100))
print(t3.fahrenheit)
