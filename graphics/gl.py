from collections import Iterable
from enum import Enum

import attr
from OpenGL.GL import (glClearColor, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_ACCUM_BUFFER_BIT,
                       GL_STENCIL_BUFFER_BIT, glClear, glShadeModel, GL_FLAT, GL_SMOOTH, GL_DEPTH_TEST, GL_CULL_FACE,
                       GL_LIGHTING, GL_LIGHT0, glEnable, glDisable, GL_LIGHT_MODEL_AMBIENT, GL_LIGHT_MODEL_TWO_SIDE,
                       GL_TRUE, GL_FALSE, glViewport, glLightModelf, glMatrixMode, GL_MODELVIEW, GL_TEXTURE,
                       GL_PROJECTION, GL_COLOR, glLoadIdentity, GL_LIGHT1, GL_LIGHT2, GL_AMBIENT, GL_DIFFUSE,
                       GL_SPECULAR, GL_POSITION, GL_SPOT_DIRECTION, GL_SPOT_EXPONENT, GL_SPOT_CUTOFF,
                       GL_CONSTANT_ATTENUATION, GL_QUADRATIC_ATTENUATION, GL_LINEAR_ATTENUATION, glLightf, glLightfv,
                       GL_COLOR_INDEXES, GL_AMBIENT_AND_DIFFUSE, GL_SHININESS, GL_EMISSION, GL_BACK, GL_FRONT,
                       GL_FRONT_AND_BACK, GL_QUADS, glBegin, glEnd, glFlush, glVertex3f, glLightModelfv, glMaterialfv,
                       glMaterialf, glBlendFunc, GL_ONE, GL_SRC_ALPHA, GL_NORMALIZE, glOrtho, GL_MAP1_VERTEX_3,
                       GL_LINE_STRIP, GL_POINTS, GL_TRIANGLES, GL_COLOR_MATERIAL, GL_LINES, glGenLists,
                       glPushMatrix, glPopMatrix, GL_COMPILE, glNewList, glEndList, glCallList, glTranslatef, glRotatef,
                       glScalef)


@attr.s(slots=True, frozen=True)
class GlColor(object):
    red = attr.ib(type=int)
    green = attr.ib(type=int)
    blue = attr.ib(type=int)

    def to_vector(self):
        return [self.red, self.green, self.blue]

    def to_float(self):
        return list(map(lambda x: x / 255, self.to_vector()))

    @property
    def value(self):
        return self.to_float()


class Gl(object):
    class Buffer(Enum):
        COLOR_BUFFER_BIT = GL_COLOR_BUFFER_BIT
        DEPTH_BUFFER_BIT = GL_DEPTH_BUFFER_BIT
        ACCUM_BUFFER_BIT = GL_ACCUM_BUFFER_BIT
        STENCIL_BUFFER_BIT = GL_STENCIL_BUFFER_BIT

    class ShadingTechnique(Enum):
        FLAT = GL_FLAT
        SMOOTH = GL_SMOOTH

    class Capability(Enum):
        CULL_FACE = GL_CULL_FACE
        DEPTH_TEST = GL_DEPTH_TEST
        LIGHTING = GL_LIGHTING
        LIGHT0 = GL_LIGHT0
        LIGHT1 = GL_LIGHT1
        LIGHT2 = GL_LIGHT2
        NORMALIZE = GL_NORMALIZE
        MAP1_VERTEX_3 = GL_MAP1_VERTEX_3
        COLOR_MATERIAL = GL_COLOR_MATERIAL

    class LightModel(Enum):
        LIGHT_MODEL_AMBIENT = GL_LIGHT_MODEL_AMBIENT
        LIGHT_MODEL_TWO_SIDE = GL_LIGHT_MODEL_TWO_SIDE

    class MatrixMode(Enum):
        MODELVIEW = GL_MODELVIEW
        PROJECTION = GL_PROJECTION
        TEXTURE = GL_TEXTURE
        COLOR = GL_COLOR

    class Bool(Enum):
        TRUE = GL_TRUE
        FALSE = GL_FALSE

    class MaterialParameter(Enum):
        AMBIENT = GL_AMBIENT
        DIFFUSE = GL_DIFFUSE
        SPECULAR = GL_SPECULAR
        EMISSION = GL_EMISSION
        SHININESS = GL_SHININESS
        AMBIENT_AND_DIFFUSE = GL_AMBIENT_AND_DIFFUSE
        COLOR_INDEXES = GL_COLOR_INDEXES

    class LightParameter(Enum):
        AMBIENT = GL_AMBIENT
        DIFFUSE = GL_DIFFUSE
        SPECULAR = GL_SPECULAR
        POSITION = GL_POSITION
        SPOT_DIRECTION = GL_SPOT_DIRECTION
        SPOT_EXPONENT = GL_SPOT_EXPONENT
        SPOT_CUTOFF = GL_SPOT_CUTOFF
        CONSTANT_ATTENUATION = GL_CONSTANT_ATTENUATION
        LINEAR_ATTENUATION = GL_LINEAR_ATTENUATION
        QUADRATIC_ATTENUATION = GL_QUADRATIC_ATTENUATION

    class MaterialFace(Enum):
        FRONT = GL_FRONT
        BACK = GL_BACK
        FRONT_AND_BACK = GL_FRONT_AND_BACK

    class BeginMode(Enum):
        QUADS = GL_QUADS
        LINE_STRIP = GL_LINE_STRIP
        POINTS = GL_POINTS
        TRIANGLES = GL_TRIANGLES
        LINES = GL_LINES

    class Factor(Enum):
        SRC_ALPHA = GL_SRC_ALPHA
        ONE = GL_ONE

    class ListMode(Enum):
        COMPILE = GL_COMPILE

    @classmethod
    def clear_color(cls, color: GlColor, alpha=1.0):
        glClearColor(*color.to_float(), alpha)

    @classmethod
    def clear(cls, *gl_buffers: Buffer):
        mask = 0
        for buffer in gl_buffers:
            mask |= buffer.value
        glClear(mask)

    @classmethod
    def shade_model(cls, mode: ShadingTechnique):
        glShadeModel(mode.value)

    @classmethod
    def enable(cls, capability: Capability):
        glEnable(capability.value)

    @classmethod
    def disable(cls, capability: Capability):
        glDisable(capability.value)

    @classmethod
    def light(cls, light: Capability, light_parameter: LightParameter, value):
        if isinstance(value, Iterable):
            glLightfv(light.value, light_parameter.value, value)
        else:
            glLightf(light.value, light_parameter.value, value)

    @classmethod
    def light_model(cls, light_model: LightModel, value):
        if isinstance(value, cls.Bool):
            glLightModelf(light_model.value, value.value)
        else:
            glLightModelfv(light_model.value, value)

    @classmethod
    def viewport(cls, x: int, y: int, width: int, height: int):
        glViewport(x, y, width, height)

    @classmethod
    def matrix_mode(cls, mode: MatrixMode):
        glMatrixMode(mode.value)

    @classmethod
    def load_identity(cls):
        glLoadIdentity()

    @classmethod
    def material(cls, face: MaterialFace, material_parameter: MaterialParameter, value):
        if isinstance(value, Iterable):
            glMaterialfv(face.value, material_parameter.value, value)
        else:
            glMaterialf(face.value, material_parameter.value, value)

    @classmethod
    def begin(cls, begin_mode: BeginMode):
        glBegin(begin_mode.value)

    @classmethod
    def end(cls):
        glEnd()

    @classmethod
    def flush(cls):
        glFlush()

    @classmethod
    def vertex3(cls, x: float, y: float, z: float):
        glVertex3f(x, y, z)

    @classmethod
    def blend_func(cls, s_factor: Factor, d_factor: Factor):
        glBlendFunc(s_factor.value, d_factor.value)

    @classmethod
    def ortho(cls, left: float, right: float, bottom: float, top: float, near: float, far: float):
        glOrtho(left, right, bottom, top, near, far)

    @classmethod
    def gen_lists(cls, number: int):
        return glGenLists(number)

    @classmethod
    def push_matrix(cls):
        glPushMatrix()

    @classmethod
    def pop_matrix(cls):
        glPopMatrix()

    @classmethod
    def new_list(cls, list_, mode: ListMode):
        glNewList(list_, mode.value)

    @classmethod
    def end_list(cls):
        glEndList()

    @classmethod
    def call_list(cls, list_):
        glCallList(list_)

    @classmethod
    def translate(cls, x: float, y: float, z: float):
        glTranslatef(x, y, z)

    @classmethod
    def rotate(cls, angle: float, x: float, y: float, z: float):
        glRotatef(angle, x, y, z)

    @classmethod
    def scale(cls, x: float, y: float, z: float):
        glScalef(x, y, z)
