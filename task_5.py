import sys

from OpenGL.GL import (glPopMatrix, glPushMatrix, glRotatef, glColor3f, glBegin, GL_POLYGON,
                       glEnd, glVertex3f, glLoadIdentity, glViewport, glTranslatef, GL_LIGHTING, glEnable, GL_LIGHT0,
                       GL_COLOR_MATERIAL, glLightfv, GL_DIFFUSE, GL_AMBIENT, GL_SPECULAR, GL_FRONT,
                       glMaterialfv, GL_SHININESS, GL_POSITION)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP, GLUT_KEY_LEFT, GLUT_KEY_RIGHT, glutSolidSphere, glutPostRedisplay

import color
from base import WindowABC, rgb_to_f


class SquareWindow(WindowABC):
    def __init__(self, title='Square', x=0, y=0, size=1.):
        super().__init__(title)
        self._x = x
        self._y = y
        self._size = size
        self._rotate_x = 0
        self._rotate_y = 0
        self._rot_grad = 5
        self._eye_x = 0
        self._eye_y = 0
        self._eye_z = 0
        self._eye_step = 5

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)

    def handle_reshape(self, width, height):
        glLoadIdentity()
        aspect = height / width

        glViewport(0, 0, width, height)

        gluPerspective(80.0, 1 / aspect, 0.1, 10000.0)

    @classmethod
    def set_light(cls):
        light_position = [1, 1, 1]
        light_ambient = [0.5, 0.5, 0.5, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    @classmethod
    def set_material(cls):
        material_ambient = [0.3, 0.5, 0.31]
        material_diffuse = [0.3, 0.3, 0.31]
        material_specular = [0.2, 0.2, 0.2, 1.0]
        material_shininess = [32.0]

        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)
        glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)

    def draw(self):
        self.handle_reshape(self.width, self.height)
        self.fill_color(0, 0, 0, 1.)
        r = self._size / 2

        self.set_light()
        self.set_material()
        gluLookAt(self._eye_x, self._eye_y, self._eye_z, 0, 0, -3 * self._size, 0, 1, 0)
        glRotatef(self._rotate_x, 1.0, 0.0, 0.0)
        glRotatef(self._rotate_y, 0.0, 1.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0, -3 * self._size)

        glPushMatrix()
        glColor3f(*rgb_to_f(*color.Blue))

        glutSolidSphere(r, 500, 500)

        glPopMatrix()

        glPushMatrix()

        glColor3f(*rgb_to_f(*color.Orange))
        h = 20 * self._size
        w = 5 * self._size
        glTranslatef(0, 0, -h)
        glBegin(GL_POLYGON)
        shift_size = - 2 * self._size
        glVertex3f(-w, shift_size, -h)
        glVertex3f(w, shift_size, -h)
        glVertex3f(w, shift_size, h)
        glVertex3f(-w, shift_size, h)
        glEnd()
        glPopMatrix()
        glPopMatrix()

    def handle_key(self, key, x, y):
        super().handle_key(key, x, y)
        key_id = ord(key)
        if key_id == 27:
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
            self._rotate_y += self._rot_grad
        elif key == GLUT_KEY_LEFT:
            self._rotate_y -= self._rot_grad
        elif key == GLUT_KEY_UP:
            self._rotate_x += self._rot_grad
        elif key == GLUT_KEY_DOWN:
            self._rotate_x -= self._rot_grad


def main():
    window = SquareWindow(size=400)
    window.show()


if __name__ == '__main__':
    main()
