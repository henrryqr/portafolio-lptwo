class Ladrillo:
    def __init__(self, longitud, altura, ancho):
        self.longitud = longitud
        self.altura = altura
        self.ancho = ancho
         
    def calcular_cantidad(self):

        return 1 / ((self.longitud + 0.015) * (self.altura + 0.015))
    
mi_ladrillo = Ladrillo(0.24, 0.09, 0.015)

print(f"La cantidad de ladrillos por m2 es (sin desperdicio): {mi_ladrillo.calcular_cantidad():}")
print(f"El area del rectangulo es (mas el desperdicio) : {mi_ladrillo.calcular_cantidad()* 1.05}")
print(f"El area del rectangulo es (mas el area de la pared) : {mi_ladrillo.calcular_cantidad()*1.05 * 8.05}")
