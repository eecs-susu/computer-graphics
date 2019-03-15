import sys
from math import cos, radians, sin

import numpy as np
from OpenGL.GL import (glBegin, glEnd, GL_POLYGON, glVertex2d,
                       glColor3f, glPushMatrix, glPopMatrix, glTranslatef, glRotatef)
from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_RIGHT_BUTTON, GLUT_KEY_LEFT, GLUT_KEY_UP, GLUT_KEY_RIGHT, GLUT_KEY_DOWN, \
    glutPostRedisplay

import color
from base import WindowABC, rgb_to_f


class RotatedSquareWindow(WindowABC):
    def __init__(self,
                 title='Square',
                 square_x=0.,
                 square_y=0.,
                 square_size=1.,
                 circle_radius=1,
                 step=1.,
                 ):
        super().__init__(title)
        self._square_x = square_x
        self._square_y = square_y
        self._circle_pos = [-self.width / 2 + circle_radius, -self.height / 2 + circle_radius]
        self._square_size = square_size
        self._circle_radius = circle_radius
        self._angle = 0
        self._should_rotate = False
        self._step = step

    def handle_idle(self):
        if self._should_rotate:
            self._angle -= 1
            glutPostRedisplay()

    def draw(self):
        self._draw_square()

        glPushMatrix()
        glColor3f(*rgb_to_f(*color.Orange))
        glTranslatef(*self._circle_pos, 0)
        glBegin(GL_POLYGON)
        for grad in np.linspace(0, 360, 1000):
            rad = radians(grad)
            x = self._circle_radius * cos(rad)
            y = self._circle_radius * sin(rad)
            glVertex2d(x, y)

        glEnd()
        glPopMatrix()

    def _draw_square(self):
        glPushMatrix()
        glColor3f(*rgb_to_f(*color.Blue))
        glTranslatef(self._square_x, self._square_y, 0)
        glRotatef(self._angle, 0, 0, 1.)
        glBegin(GL_POLYGON)
        size = self._square_size / 2
        square_vertices = [
            (size, size),
            (size, - size),
            (- size, - size),
            (- size, size),
        ]
        for square_vertex in square_vertices:
            glVertex2d(*square_vertex)
        glEnd()
        glPopMatrix()

    def handle_key(self, key, x, y):
        super().handle_key(key, x, y)
        if ord(key) == 27:
            sys.exit(0)

    def handle_special_key(self, key, x, y):
        super().handle_special_key(key, x, y)
        if key == GLUT_KEY_LEFT:
            self._circle_pos[0] -= self._step
        elif key == GLUT_KEY_UP:
            self._circle_pos[1] += self._step
        elif key == GLUT_KEY_RIGHT:
            self._circle_pos[0] += self._step
        elif key == GLUT_KEY_DOWN:
            self._circle_pos[1] -= self._step
        glutPostRedisplay()

    def handle_mouse(self, button, state, x, y):
        super().handle_mouse(button, state, x, y)
        if button == GLUT_LEFT_BUTTON:
            self._should_rotate = True
        elif button == GLUT_RIGHT_BUTTON:
            self._should_rotate = False


def main():
    window = RotatedSquareWindow(square_x=.5, square_y=.5, square_size=200, circle_radius=50, step=10)
    window.show()


if __name__ == '__main__':
    main()
