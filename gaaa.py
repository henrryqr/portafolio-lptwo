import matplotlib.pyplot as plt
import numpy as np

class FuncionLineal:
    def __init__(self, pendiente, intercepto, etiqueta):
        self.m = pendiente
        self.b = intercepto
        self.etiqueta = etiqueta
    
    def evaluar(self, x):
        return self.m * x + self.b

    def graficar(self, x_range):
        y = self.evaluar(x_range)
        plt.plot(x_range, y, label=self.etiqueta)

# Crear objetos de funciones lineales
f1 = FuncionLineal(2, 1, "f(x) = 2x + 1")
f2 = FuncionLineal(-1, 4, "g(x) = -x + 4")

# Rango de valores de x
x = np.linspace(-10, 10, 400)

# Graficar
f1.graficar(x)
f2.graficar(x)

plt.title("Gráficas de dos funciones lineales")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
