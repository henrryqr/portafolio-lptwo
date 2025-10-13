class CalculadoraEstadistica:
    def __init__(self):
        self.datos = []

    # Acción: ingresar datos
    def ingresar_datos(self, lista):
        if isinstance(lista, list):
            self.datos = lista
        else:
            raise ValueError("Debes ingresar una lista de números.")

    # Mostrar datos
    def mostrar_datos(self):
        return self.datos

    # Calcular media
    def media(self):
        if not self.datos:
            return None
        return sum(self.datos) / len(self.datos)

    # Calcular varianza (muestral)
    def varianza(self):
        n = len(self.datos)
        if n <= 1:
            return None
        media = self.media()
        suma_cuadrados = sum((x - media) ** 2 for x in self.datos)
        return suma_cuadrados / (n - 1)

    # Calcular desviación estándar
    def desviacion_estandar(self):
        var = self.varianza()
        return var ** 0.5 if var is not None else None


# Ejemplo de uso
if __name__ == "__main__":
    calc = CalculadoraEstadistica()

    # Ingresar datos
    lista = [5, 10, 10, 8, 7, 10, 6]
    calc.ingresar_datos(lista)

    print("Datos ingresados:", calc.mostrar_datos())
    print("Media:", calc.media())
    print("Varianza:", calc.varianza())
    print("Desviación estándar:", calc.desviacion_estandar())
