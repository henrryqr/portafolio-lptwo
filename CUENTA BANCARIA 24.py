class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def get_nombre(self):
        return self.nombre

    def get_precio(self):
        return self.precio

    def set_nombre(self, nuevo_nombre):
        if nuevo_nombre == "":
            print("El nombre no puede estar vacío")
        else:
            self.nombre = nuevo_nombre

    def set_precio(self, valor):
        if valor < 0:
            print("El precio no puede ser negativo")
        else:
            self.precio = valor

    def aplicar_descuento(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            print("Descuento inválido")
            return
        descuento = self.precio * (porcentaje / 100)
        self.precio = self.precio - descuento

    def mostrar(self):
        print("Producto:", self.nombre)
        print("Precio: S/.", self.precio)


p1 = Producto("Teclado", 150)
p1.mostrar()
p1.aplicar_descuento(20)
p1.mostrar()
p1.aplicar_descuento(150)
p1.set_precio(-50)
p1.set_precio(80)
p1.set_nombre("Teclado Gamer")
p1.mostrar()
