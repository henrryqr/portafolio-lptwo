# 1 # Parte 1: Importar librerías
# 2 from OpenGL.GL import *
# 3 from OpenGL.GLU import *
# 4 from OpenGL.GLUT import *
# 5 
# 6 def inicializar():
# 7     # 7 Inicializar el entorno OpenGL
# 8     glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo gris oscuro
# 9     glMatrixMode(GL_PROJECTION)
# 10    glLoadIdentity()
# 11    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0) # Vista ortográfica 2D
# 12
# 13 def dibujar_triangulo():
# 14    # 14 Dibuja el triángulo usando primitivas
# 15    glClear(GL_COLOR_BUFFER_BIT)
# 16
# 17    glColor3f(1.0, 1.0, 0.0) # Color amarillo
# 18    glBegin(GL_POINTS)
# 19
# 20    # 20 Tres vértices del triángulo
# 21    glVertex2f(0.0, 0.5) # Vértice superior
# 22    glVertex2f(-0.5, -0.5) # Vértice inferior izquierda
# 23    glVertex2f(0.5, -0.5) # Vértice inferior derecha
# 24
# 25    glEnd()
# 26    glFlush()
# 27
# 28 def main():
# 29    glutInit()
# 30    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
# 31    glutInitWindowSize(400, 400)
# 32    glutInitWindowPosition(100, 100)
# 33    glutCreateWindow("Triangulo de puntos en OpenGL")
# 34    inicializar()
# 35    glutDisplayFunc(dibujar_triangulo)
# 36    glutMainLoop()
# 37
# 38 if _name_ == '_main_':
# 39    main()
