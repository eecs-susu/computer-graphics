import sys
from abc import ABC, abstractmethod

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT
from OpenGL.GLUT import (glutInit, GLUT_RGB, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow,
                         glutInitWindowPosition, glutGet, GLUT_SCREEN_WIDTH, GLUT_SCREEN_HEIGHT, glutMainLoop,
                         GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT, glutKeyboardFunc, glutDisplayFunc, GLUT_DOUBLE,
                         glutSwapBuffers)


class WindowABC(ABC):
    def __init__(self, title, width=1024, height=768):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(width, height)
        glutInitWindowPosition((self.screen_width - width) // 2, (self.screen_height - height) // 2)
        glutCreateWindow(title)

        glutKeyboardFunc(self.handle_key)
        glutDisplayFunc(self._draw)

    def handle_key(self, key, x, y):
        pass

    @classmethod
    def clear_color_buffer(cls):
        glClear(GL_COLOR_BUFFER_BIT)

    def _draw(self):
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


def rgb_to_f(red, green, blue):
    return red / 255, green / 255, blue / 255
