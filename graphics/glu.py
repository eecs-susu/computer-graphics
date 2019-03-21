from OpenGL.raw.GLU import (gluPerspective, gluLookAt)


class Glu(object):
    @classmethod
    def perspective(cls, field_of_view_y: float, aspect: float, z_near: float, z_far: float):
        gluPerspective(field_of_view_y, aspect, z_near, z_far)

    @classmethod
    def look_at(cls, eye_x: float, eye_y: float, eye_z: float,
                center_x: float, center_y: float, center_z: float,
                up_x: float = 0., up_y: float = 1., up_z: float = 0.):
        gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z)
