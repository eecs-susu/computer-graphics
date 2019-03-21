import sys

import numpy
from OpenGL.GL import (glColor3f, glBegin, GL_POLYGON, glEnd,
                       glVertex3f, glRotatef, glPushMatrix, glPopMatrix, glTranslatef, glLoadIdentity, glViewport,
                       glBindTexture, glGenTextures, GL_TEXTURE_2D, glTexParameteri, GL_TEXTURE_WRAP_S, GL_REPEAT,
                       GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_TEXTURE_MAG_FILTER, GL_RGB,
                       GL_UNSIGNED_BYTE, glEnable, glTexImage2D, glTexCoord2f)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import GLUT_KEY_RIGHT, GLUT_KEY_LEFT, GLUT_KEY_UP, GLUT_KEY_DOWN, glutPostRedisplay
from PIL import Image

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

        self._textures = [
            self.load_texture('images/ray.bmp'),
            self.load_texture('images/flower.jpg'),
            self.load_texture('images/plane.jpg'),
        ]

    @classmethod
    def load_texture(cls, file_name):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # load image
        image = Image.open(file_name)
        img_data = numpy.array(list(image.getdata()), numpy.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)
        return texture

    def handle_reshape(self, width, height):
        glLoadIdentity()
        aspect = height / width

        glViewport(0, 0, width, height)

        gluPerspective(45.0, 1 / aspect, 0.1, 2000.0)

    def _draw_zero_plane_xy(self, color, texture_id=None, scale=1.0):
        glPushMatrix()
        # glColor3f(*rgb_to_f(*color))
        apply_texture = texture_id is not None
        if apply_texture:
            glColor3f(1, 1, 1)
            glBindTexture(GL_TEXTURE_2D, self._textures[texture_id])
            glTexCoord2f(1.0 * scale, 0.0 * scale)
        else:
            glColor3f(*rgb_to_f(*color))
        glBegin(GL_POLYGON)
        size = self._size / 2

        glVertex3f(size, size, 0)
        if apply_texture:
            glTexCoord2f(1.0 * scale, 1.0 * scale)
        glVertex3f(size, -size, 0)
        if apply_texture:
            glTexCoord2f(0.0 * scale, 1.0 * scale)
        glVertex3f(-size, -size, 0)
        if apply_texture:
            glTexCoord2f(0.0 * scale, 0.0 * scale)
        glVertex3f(-size, size, 0)
        # if texture is not None:
        #     glBindTexture(GL_TEXTURE_2D, )
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
        self._draw_zero_plane_xy(Color.Blue, 0, 2)
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
        self._draw_zero_plane_xy(Color.Purple, 2)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-size, 0, 0)
        glRotatef(90, 0, 1, 0)
        self._draw_zero_plane_xy(Color.Red, 1)
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
