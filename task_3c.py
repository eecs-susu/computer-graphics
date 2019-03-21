import sys

from OpenGL.GL import (glColor3f, glBegin, GL_POLYGON, glEnd,
                       glVertex3f, glRotatef, glPushMatrix, glPopMatrix, glTranslatef, glLoadIdentity, glViewport)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import GLUT_KEY_RIGHT, GLUT_KEY_LEFT, GLUT_KEY_UP, GLUT_KEY_DOWN, glutPostRedisplay

import color as Color
from base import WindowABC, rgb_to_f


class CubeWindow(WindowABC):
    def __init__(self, title='Square', x=0., y=0., z=0., size=1.):
        super().__init__(title)
        self._x = x
        self._y = y
        self._z = z
        self._size = size
        self._rotate_x = 0.
        self._rotate_y = 0.
        self._eye_x = 0
        self._eye_y = 0
        self._eye_z = 0
        self._eye_step = 100

    def handle_reshape(self, width, height):
        glLoadIdentity()
        aspect = height / width

        glViewport(0, 0, width, height)

        gluPerspective(45.0, 1 / aspect, 0.1, 2000.0)

    def _draw_xy_edge(self, color):
        glColor3f(*rgb_to_f(*color))
        glBegin(GL_POLYGON)

        size = self._size / 2
        glVertex3f(size, size, 0.)
        glVertex3f(size, -size, 0.)
        glVertex3f(-size, -size, 0.)
        glVertex3f(-size, size, 0.)
        glEnd()

    def _draw_yz_edge(self, color):
        glBegin(GL_POLYGON)
        glColor3f(*rgb_to_f(*color))
        size = self._size / 2
        glVertex3f(size, size, 0.)
        glVertex3f(size, -size, 0.)
        glVertex3f(-size, -size, 0.)
        glVertex3f(-size, size, 0.)
        glEnd()

    def _draw_front_edge(self, color):
        glPushMatrix()

        glTranslatef(self._x, self._y, self._z)
        self._draw_xy_edge(color)
        glPopMatrix()

    def _draw_back_edge(self, color):
        glPushMatrix()
        glTranslatef(0, 0, self._size)
        self._draw_xy_edge(color)
        glPopMatrix()

    def _draw_zero_plane_xy(self, color):
        glPushMatrix()
        glColor3f(*rgb_to_f(*color))
        glBegin(GL_POLYGON)
        size = self._size / 2
        glVertex3f(size, size, 0)
        glVertex3f(size, -size, 0)
        glVertex3f(-size, -size, 0)
        glVertex3f(-size, size, 0)
        glEnd()
        glPopMatrix()

    def draw(self):

        self.handle_reshape(self.width, self.height)
        size = self._size / 2

        glPushMatrix()

        glTranslatef(0, 0, -5.64 * size)

        gluLookAt(self._eye_x, self._eye_y, self._eye_z, 0, 0, -5.64 * size, 0, 1, 0)

        glRotatef(self._rotate_x, 1.0, 0.0, 0.0)
        glRotatef(self._rotate_y, 0.0, 1.0, 0.0)

        glPushMatrix()
        glTranslatef(0, 0, size)
        self._draw_zero_plane_xy(Color.Blue)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, -size)
        self._draw_zero_plane_xy(Color.Orange)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, size, 0)
        glRotatef(90, 1, 0, 0)
        self._draw_zero_plane_xy(Color.Green)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, -size, 0)
        glRotatef(90, 1, 0, 0)
        self._draw_zero_plane_xy(Color.Pink)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(size, 0, 0)
        glRotatef(90, 0, 1, 0)
        self._draw_zero_plane_xy(Color.Purple)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-size, 0, 0)
        glRotatef(90, 0, 1, 0)
        self._draw_zero_plane_xy(Color.Red)
        glPopMatrix()

        glPopMatrix()

    def handle_key(self, key, x, y):
        super().handle_key(key, x, y)
        key_id = ord(key)
        if key_id == 27:  # ESC
            sys.exit(0)
        elif key_id == 91:  # [
            self._eye_x -= self._eye_step
        elif key_id == 93:  # ]
            self._eye_x += self._eye_step
        elif key_id == 39:  # '
            self._eye_y -= self._eye_step
        elif key_id == 92:  # \
            self._eye_y += self._eye_step
        elif key_id == 46:  # .
            self._eye_z -= self._eye_step
        elif key_id == 47:  # /
            self._eye_z += self._eye_step
        glutPostRedisplay()

    def handle_special_key(self, key, x, y):
        super().handle_special_key(key, x, y)
        if key == GLUT_KEY_RIGHT:
            self._rotate_y += 1
        elif key == GLUT_KEY_LEFT:
            self._rotate_y -= 1
        elif key == GLUT_KEY_UP:
            self._rotate_x += 1
        elif key == GLUT_KEY_DOWN:
            self._rotate_x -= 1
        glutPostRedisplay()


def main():
    window = CubeWindow(size=400)
    window.show()


if __name__ == '__main__':
    main()
