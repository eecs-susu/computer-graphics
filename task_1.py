import sys

from OpenGL.GL import (glBegin, glEnd, GL_POLYGON, glVertex2d,
                       glColor3f)

from base import WindowABC, rgb_to_f

BACKGROUND_COLOR = (250, 250, 250)
ACCENT_COLOR = (0, 122, 255)


class SquareWindow(WindowABC):
    def __init__(self, title='Square', x=0, y=0, size=1.):
        super().__init__(title)
        self._x = x
        self._y = y
        self._size = size

    def draw(self):
        self.fill_color(*BACKGROUND_COLOR, 1)
        self.clear_color_buffer()

        ratio = self.width / self.height
        size_y = self._size * ratio

        dx = self._size / 2
        dy = size_y / 2

        glColor3f(*rgb_to_f(0, 122, 255))

        glBegin(GL_POLYGON)

        glVertex2d(self._x + dx, self._y + dy)
        glVertex2d(self._x + dx, self._y - dy)
        glVertex2d(self._x - dx, self._y - dy)
        glVertex2d(self._x - dx, self._y + dy)

        glEnd()

    def handle_key(self, key, x, y):
        super().handle_key(key, x, y)
        if ord(key) == 27:
            sys.exit(0)


def main():
    window = SquareWindow(size=0.5)
    window.show()


if __name__ == '__main__':
    main()
