from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def inicializar():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -5, 5, -1, 1)

def dibujar_letras():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)

    # Letra U
    glVertex2f(-9, 4)
    glVertex2f(-9, -2)
    glVertex2f(-9, -2)
    glVertex2f(-6, -2)
    glVertex2f(-6, -2)
    glVertex2f(-6, 4)

    # Letra N cruzando el eje X
    glVertex2f(-3, -2)
    glVertex2f(-3, 4)
    glVertex2f(-3, 4)
    glVertex2f(3, -2)
    glVertex2f(3, -2)
    glVertex2f(3, 4)

    # Letra A
    glVertex2f(6, -2)
    glVertex2f(6, 4)
    glVertex2f(6, 4)
    glVertex2f(5, -2)
    glVertex2f(2.75, 1)
    glVertex2f(9, -2)

    glEnd()
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Dibujando UNA con N cruzada")
    inicializar()
    glutDisplayFunc(dibujar_letras)
    glutMainLoop()

if __name__ == "__main__":
    main()
