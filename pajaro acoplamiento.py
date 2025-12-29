class pajaro:
    def mover(self):
        print("el pajaro vuela")

class pez:
    def mover(self):
        print("el pez nada")
class persona:
    def mover(self):
        print("la persona camina")

def desplazar(objeto):
    objeto.mover()
objetos=[pajaro(), pez(), persona()]

for objeto in objetos:
    desplazar(objeto)
