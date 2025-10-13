class coche:
    def __init__(self,marca,modelo,color):
       self.marca = marca
       self.modelo = modelo
       self.color = color
       
    def mostrar_info(self):
        print(f"coche:{self.marca} {self.modelo} {self.color}")
    
    def arrancar(self):
        print(f"coche {self.marca} {self.modelo} ha arrancado ")


#solicitar daros al usuario
marca = input("ingrese la marca del coche :")
modelo = input("ingrese el modelo del auto :")
color = input ("ingrese el color del coche :")

#crear un objeto

mi_coche = coche(marca, modelo, color)

#usar los metodos del objeto

mi_coche.mostrar_info()
mi_coche.arrancar()
