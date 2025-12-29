class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = float(salario)

    def calcular_pago(self):
        return 0


class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = float(salario)

    def calcular_pago(self):
        return self.salario


class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, pago_hora, horas):
        self.nombre = nombre
        self.salario = float(pago_hora)
        self.horas = horas

    def calcular_pago(self):
        return self.salario * self.horas


empleados = [
    EmpleadoTiempoCompleto("Luis", 1500),
    EmpleadoPorHoras("Ana", 12, 80),
    EmpleadoTiempoCompleto("Carlos", 1800),
    EmpleadoPorHoras("Pedro", 10, 100)
]

for e in empleados:
    print(e.nombre, e.calcular_pago())
