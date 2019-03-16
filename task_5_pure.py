import sys
from math import sin, cos, pi, radians

import numpy as np

from graphics import (
    gl,
    glu,
    glut,
    GlColor,
)

INITIAL_WINDOW_SIZE = (1024, 768)
TITLE = 'Lighting'

RED_COLOR = GlColor(255, 59, 48)
ORANGE_COLOR = GlColor(255, 149, 0)
YELLOW_COLOR = GlColor(255, 204, 0)
GREEN_COLOR = GlColor(76, 217, 100)
TEAL_BLUE_COLOR = GlColor(90, 200, 250)
BLUE_COLOR = GlColor(0, 122, 255)
PURPLE_COLOR = GlColor(88, 86, 214)
PINK_COLOR = GlColor(255, 45, 85)
WHITE_COLOR = GlColor(255, 255, 255)
SMOKE_COLOR = GlColor(250, 250, 250)


class Settings(object):
    field_of_view_y = 60  # degrees

    z_near = 0.0001
    z_far = 100

    view_radius = 3.0
    view_theta = - 3 * pi / 2
    view_phi = - pi / 2
    view_delta_rad = radians(5)

    sphere_center = [0, 0, 0]

    light_intensity = 0.2

    projection_enabled = True

    projection_light_diffuse = [1.0, 1.0, 1.0]
    projection_light_position = [0.0, 0.0, -1.0, 1.0]
    projection_light_spot_cutoff = 15.0
    projection_light_spot_direction = [0.0, 0.0, 1.0]
    projection_light_spot_exponent = 30.0

    point_light_diffuse = [1.0, 1.0, 1.0]
    point_light_position = [0.0, 0.0, -1.0, 1]
    point_light_constant_attenuation = 0.0
    point_light_linear_attenuation = 0.2
    point_light_quadratic_attenuation = 0.2

    sphere_material = [1.0, 0.0, 0.0, 1.0]
    sphere_radius = 0.2
    sphere_detailing = 500

    wall_material = [0.4, 0.7, 0.2, 1.0]
    wall_z = 0.8
    wall_size = 2
    wall_step = 0.005

    @property
    def light_ambient(self):
        return [self.light_intensity, self.light_intensity, self.light_intensity, 1]

    @property
    def sphere_solid_parameters(self):
        return [self.sphere_radius, self.sphere_detailing, self.sphere_detailing]


settings = Settings()


def get_window_center(width=None, height=None):
    width = width or glut.get_window_width()
    height = height or glut.get_window_height()
    x = glut.get_screen_width() - width
    y = glut.get_screen_height() - height
    return x >> 1, y >> 1


def display_callback():
    gl.clear(gl.Buffer.COLOR_BUFFER_BIT, gl.Buffer.DEPTH_BUFFER_BIT)
    gl.load_identity()

    x_eye = settings.sphere_center[0] + settings.view_radius * sin(settings.view_theta) * cos(settings.view_phi)
    z_eye = settings.sphere_center[0] + settings.view_radius * sin(settings.view_theta) * sin(settings.view_phi)
    y_eye = settings.sphere_center[0] + settings.view_radius * cos(settings.view_theta)

    glu.look_at(x_eye, y_eye, z_eye, *settings.sphere_center)

    gl.light_model(gl.LightModel.LIGHT_MODEL_AMBIENT, settings.light_ambient)

    if settings.projection_enabled:
        gl.enable(gl.Capability.LIGHT1)

        gl.light(gl.Capability.LIGHT1, gl.LightParameter.DIFFUSE, settings.projection_light_diffuse)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.POSITION, settings.projection_light_position)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_CUTOFF, settings.projection_light_spot_cutoff)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_DIRECTION, settings.projection_light_spot_direction)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_EXPONENT, settings.projection_light_spot_exponent)
    else:
        gl.enable(gl.Capability.LIGHT0)

        gl.light(gl.Capability.LIGHT0, gl.LightParameter.DIFFUSE, settings.point_light_diffuse)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.POSITION, settings.point_light_position)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.CONSTANT_ATTENUATION,
                 settings.point_light_constant_attenuation)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.LINEAR_ATTENUATION, settings.point_light_linear_attenuation)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.QUADRATIC_ATTENUATION,
                 settings.point_light_quadratic_attenuation)

    gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.sphere_material)

    glut.solid_sphere(*settings.sphere_solid_parameters)

    gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.wall_material)

    gl.begin(gl.BeginMode.QUADS)

    min_edge = -settings.wall_size / 2
    max_edge = -min_edge

    for wall_x in np.arange(min_edge, max_edge, settings.wall_step):
        for wall_y in np.arange(min_edge, max_edge, settings.wall_step):
            gl.vertex3(wall_x, wall_y, settings.wall_z)
            gl.vertex3(wall_x, wall_y + settings.wall_step, settings.wall_z)
            gl.vertex3(wall_x + settings.wall_step, wall_y + settings.wall_step, settings.wall_z)
            gl.vertex3(wall_x + settings.wall_step, wall_y, settings.wall_z)

    gl.end()

    gl.flush()

    gl.disable(gl.Capability.LIGHT0)
    gl.disable(gl.Capability.LIGHT1)

    glut.swap_buffers()


def reshape_callback(width, height):
    gl.viewport(0, 0, width, height)
    gl.matrix_mode(gl.MatrixMode.PROJECTION)
    gl.load_identity()
    aspect = width / height
    glu.perspective(settings.field_of_view_y, aspect, settings.z_near, settings.z_far)
    gl.matrix_mode(gl.MatrixMode.MODELVIEW)
    gl.load_identity()


def keyboard_callback(key, x, y):
    if key == b'\x1b':  # ESC
        sys.exit(0)
    elif key == b'[':
        settings.view_phi += settings.view_delta_rad
    elif key == b']':
        settings.view_phi -= settings.view_delta_rad
    elif key == b' ':
        settings.projection_enabled = not settings.projection_enabled
    glut.post_redisplay()


def main():
    glut.init(sys.argv)
    glut.init_display_mode(glut.DisplayMode.DEPTH, glut.DisplayMode.RGB, glut.DisplayMode.DOUBLE)
    glut.init_window_size(*INITIAL_WINDOW_SIZE)
    glut.init_window_position(*get_window_center(*INITIAL_WINDOW_SIZE))
    glut.create_window(TITLE)

    gl.shade_model(gl.ShadingTechnique.SMOOTH)

    gl.enable(gl.Capability.CULL_FACE)
    gl.enable(gl.Capability.DEPTH_TEST)
    gl.enable(gl.Capability.LIGHTING)

    gl.light_model(gl.LightModel.LIGHT_MODEL_TWO_SIDE, gl.Bool.TRUE)

    glut.display_func(display_callback)
    glut.reshape_func(reshape_callback)
    glut.keyboard_func(keyboard_callback)

    glut.main_loop()


if __name__ == '__main__':
    main()
