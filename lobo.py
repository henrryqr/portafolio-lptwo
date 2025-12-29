from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Coordenadas del lobo
vertices_contorno = [
    (-9, 7), (-8, 10), (-7, 10), (-7, 9), (-5, 9), (-3, 7), (-2, 6),
    (0, 7), (2, 6), (3, 7), (5, 9), (7, 9), (8, 10), (7, 10), (5, 9),
    (7, 9), (9, 7), (8, 4), (7, 1), (8, -3), (9, -7), (8, -7), (7, -6),
    (4, -5), (3, -6), (3, -7), (4, -9), (1, -10), (-1, -10), (-4, -9),
    (-3, -7), (-3, -6), (-4, -5), (-7, -6), (-8, -7), (-9, -6), (-8, -2),
    (-7, 1), (-8, 4), (-9, 7)
]

# Polígonos rellenos
poligono_izq = [(-7, 9), (-7, 10), (-8, 10), (-9, 7), (-8, 4), (-7, 4), (-4, 6), (-7, 9)]
poligono_der = [(5, 9), (7, 10), (8, 10), (9, 7), (8, 4), (7, 5), (4, 6), (5, 9)]
hexagono = [(-2, -6), (-1, -8), (1, -8), (2, -6), (1, -5), (-1, -5)]

# Líneas internas
lineas_internas = [
    # Zona superior
    [(-7, 9), (-4, 6)], [(-4, 6), (-3, 4)], [(-3, 4), (0, 1)],
    [(0, 1), (3, 4)], [(3, 4), (4, 6)], [(4, 6), (7, 9)],
    [(-4, 6), (-2, 6)], [(4, 6), (2, 6)], [(-2, 6), (0, 7)], [(0, 7), (2, 6)],
    
    # Conexiones medias
    [(-7, 4), (-8, 4)], [(7, 5), (8, 4)], [(-7, 1), (-7, 4)], [(7, 1), (7, 5)],
    
    # Zona inferior izquierda
    [(0, 1), (-1, 0)], [(-1, 0), (-4, 0)], [(-4, 0), (-5, 0)],
    [(-5, 0), (-5, -3)], [(-5, -3), (-4, -5)], [(-4, -5), (-3, -6)],
    [(-4, 0), (-4, -1)], [(-4, -1), (-3, -4)], [(-3, -4), (-2, -4)], [(-2, -4), (0, 1)],
    
    # Zona inferior derecha
    [(0, 1), (1, 0)], [(1, 0), (4, 0)], [(4, 0), (5, 0)],
    [(5, 0), (5, -3)], [(5, -3), (4, -5)], [(4, -5), (3, -6)],
    [(4, 0), (4, -1)], [(4, -1), (3, -4)], [(3, -4), (2, -4)], [(2, -4), (0, 1)],
    
    # Hexágono conexiones
    [(-2, -4), (-2, -6)], [(2, -4), (2, -6)], [(-1, -5), (-1, -8)], [(1, -5), (1, -8)],
]

def inicializar():
    """Configura el entorno OpenGL"""
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-12.0, 12.0, -12.0, 12.0, -1.0, 1.0)  # Vista ortográfica 2D

def dibujar_cuadricula():
    """Dibuja la cuadrícula de fondo"""
    glColor3f(0.9, 0.9, 0.9)
    glLineWidth(1.0)
    
    # Líneas verticales y horizontales
    glBegin(GL_LINES)
    for i in range(-12, 13):
        glVertex2f(i, -12)
        glVertex2f(i, 12)
        glVertex2f(-12, i)
        glVertex2f(12, i)
    glEnd()
    
    # Ejes principales
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(-12, 0)
    glVertex2f(12, 0)
    glVertex2f(0, -12)
    glVertex2f(0, 12)
    glEnd()

def dibujar_poligono_relleno(poligono, r, g, b):
    """Dibuja un polígono relleno"""
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    for x, y in poligono:
        glVertex2f(x, y)
    glEnd()

def dibujar_lobo():
    """Dibuja el lobo completo"""
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Dibujar cuadrícula
    dibujar_cuadricula()
    
    # Dibujar polígonos rellenos (gris claro)
    dibujar_poligono_relleno(poligono_izq, 0.7, 0.7, 0.7)
    dibujar_poligono_relleno(poligono_der, 0.7, 0.7, 0.7)
    dibujar_poligono_relleno(hexagono, 0.7, 0.7, 0.7)
    
    # Dibujar contorno principal
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.5)
    glBegin(GL_LINE_LOOP)
    for x, y in vertices_contorno:
        glVertex2f(x, y)
    glEnd()
    
    # Dibujar líneas internas
    glLineWidth(1.5)
    glBegin(GL_LINES)
    for linea in lineas_internas:
        glVertex2f(linea[0][0], linea[0][1])
        glVertex2f(linea[1][0], linea[1][1])
    glEnd()
    
    # Dibujar hexágono
    glBegin(GL_LINE_LOOP)
    for x, y in hexagono:
        glVertex2f(x, y)
    glEnd()
    
    # Dibujar puntos en los vértices
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for x, y in vertices_contorno:
        glVertex2f(x, y)
    # Puntos del hexágono
    for x, y in hexagono:
        glVertex2f(x, y)
    # Puntos adicionales de las líneas internas
    puntos_adicionales = [
        (-4, 6), (-3, 4), (0, 1), (3, 4), (4, 6),
        (-7, 4), (7, 5), (-1, 0), (1, 0), (-4, 0), (4, 0),
        (-5, 0), (5, 0), (-5, -3), (5, -3), (-4, -1), (4, -1),
        (-3, -4), (3, -4), (-2, -4), (2, -4)
    ]
    for x, y in puntos_adicionales:
        glVertex2f(x, y)
    glEnd()
    
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Grafica del Lobo en OpenGL")
    inicializar()
    glutDisplayFunc(dibujar_lobo)
    glutMainLoop()

if __name__ == "__main__":
    main()
