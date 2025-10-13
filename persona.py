class Persona:
    def __init__(self,nombre,edad):
        self.__nombre = nombre #atributo privado
        self.__edad = edad # atributo privado
    def get_edad(self):
        return self.__edad

    def get_nombre(self):
        return self.__nombre
    
    def set_edad(self,nueva_edad):
        if nueva_edad > 0:
            self.__edad = nueva_edad
        else:
            print("edad no valida")

    def set_nombre(self,nuevo_nombre):
         self.__nombre = nuevo_nombre
         return self.__nombre
        

persona = Persona("ANA",30)
print(persona.get_nombre())
print(persona.get_edad())
print(persona.get_nombre(), persona.get_edad() )

persona.set_edad(35)
persona.set_nombre("maria")
print (persona.get_nombre())
print (persona.get_edad())
