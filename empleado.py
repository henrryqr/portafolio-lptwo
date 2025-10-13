#clase empleado
#atributo nombre cargo salario
#accio  aplicar el aumento de sueldo (Aplicar aumento())
#gerente 10%
#supervisor 7%
#operario 5%
#otros nada
class Empleado:
    def __init__(self, nombre, cargo, salario):
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

    def AplicarAumento(self):
        if self.cargo == "Gerente":
            porcentaje = 0.10
        elif self.cargo == "Supervisor":
            porcentaje = 0.07
        elif self.cargo == "Operario":
            porcentaje = 0.05
        else:
            porcentaje = 0.0

        nuevoSalario = self.salario * (1 + porcentaje)
        return nuevoSalario
nombre = input("ingrese el nombre")
cargo = input("ingrese el cargo")
salario = float(input("ingrese el salario")

Empleado1 = Empleado("Carlos", "Gerente", 2000)
Empleado2 = Empleado("Maria", "Operario", 1200)
Empleado3 = Empleado("Ana", "Gerente", 800)
Empleado4 = Empleado("Rosa", "Supervisor", 100)

for emp in (Empleado1, Empleado2, Empleado3, Empleado4):
    salarioN = emp.AplicarAumento()
    print(f"El nuevo salario de {emp.nombre} es {salarioN:.2f}")
