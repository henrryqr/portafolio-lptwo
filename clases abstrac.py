from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def hacer_sonido(self):
        pass

    def info(self):
        return self.nombre + ": " + self.hacer_sonido()


class Perro(Animal):
    def __init__(self, nombre):
        self.nombre = nombre

    def hacer_sonido(self):
        return "Guau"


class Gato(Animal):
    def __init__(self, nombre):
        self.nombre = nombre

    def hacer_sonido(self):
        return "Miau"


class Vaca(Animal):
    def __init__(self, nombre):
        self.nombre = nombre

    def hacer_sonido(self):
        return "Muu"


class Loro(Animal):
    def __init__(self, nombre, frase):
        self.nombre = nombre
        self.frase = frase

    def hacer_sonido(self):
        return self.frase


animales = [
    Perro("Firulais"),
    Gato("Michi"),
    Vaca("Lola"),
    Loro("Pepe", "Hola hola")
]

for a in animales:
    print(a.info())
