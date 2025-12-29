class animal:
    def hacer_sonido(self):
        print("sonido generico")

class perro(animal):
    def hacer_sonido(self):
        print("guau")

class gato(animal):
    def hacer_sonido(self):
        print("miau")

animales = [perro(), gato(), animal()]

for animal in animales:
    animal.hacer_sonido()
