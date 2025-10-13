
xmin, xmax = 0, 15
ymin, ymax = 0, 15

soluciones = []


print("Región factible (F): x >= 5, y >= 0, x + y <= 15")
print("Ejes: '|' = eje Y (x=0), '-' = eje X (y=0), '+' = origen")
print()

for y in range(ymax, ymin - 1, -1):
    linea = ""
    for x in range(xmin, xmax + 1):
        
        factible = (x >= 5 and x + y <= 15 and y >= 0)

       
        frontera = (x == 5 or x + y == 15)

        if factible and frontera:
           
            linea += "B"
        elif factible:
            linea += "F"
        elif x == 0 and y == 0:
            linea += "+"
        elif x == 0:
            linea += "|"
        elif y == 0:
            linea += "-"
        else:
            linea += " "

    
        if factible:
            soluciones.append((x, y))
    print(linea)

soluciones = sorted(set(soluciones))


print("\nLeyenda: F = interior factible, B = borde factible, - = eje X, | = eje Y, + = origen")
print(f"\nHay {len(soluciones)} combinaciones enteras (x,y) con 0<=x,y<=15 que cumplen las restricciones.\n")


print("Combinaciones enteras posibles (x = horas front-end, y = horas back-end):")
for s in soluciones:
    print(s)



