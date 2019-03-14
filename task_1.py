import sys

from OpenGL.GL import (glBegin, glEnd, GL_POLYGON, glVertex2d,
                       glColor3f)

import color
from base import WindowABC, rgb_to_f


class SquareWindow(WindowABC):
    def __init__(self, title='Square', x=0, y=0, size=1.):
        super().__init__(title)
        self._x = x
        self._y = y
        self._size = size

    def draw(self):
        glColor3f(*rgb_to_f(*color.Blue))

        glBegin(GL_POLYGON)

        size = self._size * self.scale / 2
        glVertex2d(self._x + size, self._y + size)
        glVertex2d(self._x + size, self._y - size)
        glVertex2d(self._x - size, self._y - size)
        glVertex2d(self._x - size, self._y + size)

        glEnd()

    def handle_key(self, key, x, y):
        super().handle_key(key, x, y)
        if ord(key) == 27:
            sys.exit(0)


def main():
    window = SquareWindow(size=400)
    window.show()


if __name__ == '__main__':
    main()
