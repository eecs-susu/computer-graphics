from enum import Enum

from OpenGL.GLUT import (glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow,
                         glutMainLoop, glutKeyboardFunc, glutDisplayFunc, glutIdleFunc, glutMouseFunc, glutSpecialFunc,
                         glutReshapeFunc, glutGet, glutSwapBuffers, GLUT_RGB, GLUT_DOUBLE, GLUT_DEPTH,
                         GLUT_SCREEN_WIDTH, GLUT_SCREEN_HEIGHT, GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT, glutSolidSphere,
                         glutPostRedisplay)


class Glut(object):
    class State(Enum):
        SCREEN_WIDTH = GLUT_SCREEN_WIDTH
        SCREEN_HEIGHT = GLUT_SCREEN_HEIGHT
        WINDOW_WIDTH = GLUT_WINDOW_WIDTH
        WINDOW_HEIGHT = GLUT_WINDOW_HEIGHT

    class DisplayMode(Enum):
        """
        See: https://www.opengl.org/resources/libraries/glut/spec3/node12.html
        """
        RGB = GLUT_RGB
        DOUBLE = GLUT_DOUBLE
        DEPTH = GLUT_DEPTH

    @classmethod
    def init(cls, argv):
        glutInit(argv)

    @classmethod
    def init_display_mode(cls, *modes: DisplayMode):
        if not modes:
            return
        mode = 0
        for partial_mode in modes:
            mode |= partial_mode.value
        glutInitDisplayMode(mode)

    @classmethod
    def init_window_size(cls, width, height):
        glutInitWindowSize(width, height)

    @classmethod
    def init_window_position(cls, x: int, y: int):
        glutInitWindowPosition(x, y)

    @classmethod
    def create_window(cls, title):
        glutCreateWindow(title)

    @classmethod
    def main_loop(cls):
        glutMainLoop()

    @classmethod
    def keyboard_func(cls, callback):
        glutKeyboardFunc(callback)

    @classmethod
    def display_func(cls, callback):
        glutDisplayFunc(callback)

    @classmethod
    def idle_func(cls, callback):
        glutIdleFunc(callback)

    @classmethod
    def mouse_func(cls, callback):
        glutMouseFunc(callback)

    @classmethod
    def special_func(cls, callback):
        glutSpecialFunc(callback)

    @classmethod
    def reshape_func(cls, callback):
        glutReshapeFunc(callback)

    @classmethod
    def get(cls, state: State):
        return glutGet(state.value)

    @classmethod
    def get_screen_width(cls):
        return cls.get(cls.State.SCREEN_WIDTH)

    @classmethod
    def get_screen_height(cls):
        return cls.get(cls.State.SCREEN_HEIGHT)

    @classmethod
    def get_window_width(cls):
        return cls.get(cls.State.WINDOW_WIDTH)

    @classmethod
    def get_window_height(cls):
        return cls.get(cls.State.WINDOW_HEIGHT)

    @classmethod
    def swap_buffers(cls):
        glutSwapBuffers()

    @classmethod
    def solid_sphere(cls, radius: float, slices: int, stacks: int):
        glutSolidSphere(radius, slices, stacks)

    @classmethod
    def post_redisplay(cls):
        glutPostRedisplay()
