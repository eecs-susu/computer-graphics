import sys
from abc import ABC, abstractmethod

from OpenGL.GL import (glClearColor, glClear, GL_COLOR_BUFFER_BIT, glEnable, GL_DEPTH_TEST, GL_DEPTH_BUFFER_BIT,
                       glLoadIdentity, glViewport, glOrtho)
from OpenGL.GLUT import (glutInit, GLUT_RGB, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow,
                         glutInitWindowPosition, glutGet, GLUT_SCREEN_WIDTH, GLUT_SCREEN_HEIGHT, glutMainLoop,
                         GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT, glutKeyboardFunc, glutDisplayFunc, GLUT_DOUBLE,
                         glutSwapBuffers, glutIdleFunc, glutMouseFunc, glutSpecialFunc, GLUT_DEPTH,
                         glutReshapeFunc)

import color


class WindowABC(ABC):
    def __init__(self, title, width=1024, height=768):
        self.base_width = width
        self.base_height = height

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition((self.screen_width - width) // 2, (self.screen_height - height) // 2)
        glutCreateWindow(title)

        glutKeyboardFunc(self.handle_key)
        glutDisplayFunc(self._draw)
        glutIdleFunc(self.handle_idle)
        glutMouseFunc(self.handle_mouse)
        glutSpecialFunc(self.handle_special_key)
        glutReshapeFunc(self.handle_reshape)

        glEnable(GL_DEPTH_TEST)

    def handle_reshape(self, width, height):
        glLoadIdentity()
        aspect = height / width

        glViewport(0, 0, width, height)
        bw = self.width / 2
        glOrtho(-bw, bw, -bw * aspect, bw * aspect, -bw, bw)

    def handle_mouse(self, button, state, x, y):
        pass

    def handle_key(self, key, x, y):
        pass

    def handle_special_key(self, key, x, y):
        pass

    @classmethod
    def clear_color_buffer(cls):
        glClear(GL_COLOR_BUFFER_BIT)

    @classmethod
    def clear_depth_buffer(cls):
        glClear(GL_DEPTH_BUFFER_BIT)

    def handle_idle(self):
        pass

    def _draw(self):
        self.fill_color(*color.Smoke, 1.)
        self.clear_color_buffer()
        self.clear_depth_buffer()
        self.draw()
        glutSwapBuffers()

    @abstractmethod
    def draw(self):
        pass

    @property
    def screen_width(self):
        return glutGet(GLUT_SCREEN_WIDTH)

    @property
    def screen_height(self):
        return glutGet(GLUT_SCREEN_HEIGHT)

    @property
    def width(self):
        return glutGet(GLUT_WINDOW_WIDTH)

    @property
    def height(self):
        return glutGet(GLUT_WINDOW_HEIGHT)

    @staticmethod
    def show():
        glutMainLoop()

    @classmethod
    def fill_color(cls, red, green, blue, alpha=1.):
        assert 0 <= red <= 255
        assert 0 <= green <= 255
        assert 0 <= blue <= 255
        assert 0. <= alpha <= 1.
        glClearColor(*rgb_to_f(red, green, blue), alpha)

    @property
    def scale(self):
        scale_x = self.width / self.base_width
        scale_y = self.height / self.base_height
        return scale_x * scale_y


def rgb_to_f(red, green, blue):
    return red / 255, green / 255, blue / 255
