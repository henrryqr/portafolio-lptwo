import gc

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        print(f"Producto registrado: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}")

    def mostrar_informacion(self):
        print(f"Producto: {self.nombre} | Precio: {self.precio} | Cantidad: {self.cantidad}")

    def __del__(self):
        print(f"Producto eliminado: {self.nombre}")


n = int(input("¿Cuántos productos deseas registrar? "))

producto_datos = []
for i in range(n):
    print(f"\n--- Registro de producto {i+1} ---")
    nombre = input("Nombre: ")
    precio = input("Precio: ")
    cantidad = input("Cantidad: ")
    producto = Producto(nombre, precio, cantidad)
    producto_datos.append(producto)

inventario = []
for datos in producto_datos:
    datos.mostrar_informacion() 
    inventario.append(datos)      

inventario.clear()
del producto
gc.collect()

print("\nFin del programa")
