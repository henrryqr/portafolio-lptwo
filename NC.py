class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def get_precio(self):
        return self.precio

    def set_precio(self, valor):
        if valor < 0:
            print("El precio no puede ser negativo")
        else:
            self.precio = valor

    def aplicar_descuento(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            print("Descuento inválido")
            return
        self.precio = self.precio - (self.precio * porcentaje / 100)


p = Producto("Mouse", 80)
print(p.get_precio())
p.aplicar_descuento(20)
print(p.get_precio())
p.aplicar_descuento(150)
print(p.get_precio())
