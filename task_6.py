import sys
from math import sin, cos, pi, sqrt

import numpy as np
from OpenGL.GLUT import glutSetOption

from graphics import (
    gl,
    glu,
    glut)
from task_6_helper import Settings, Particle, PINK_COLOR

INITIAL_WINDOW_SIZE = (1024, 768)
TITLE = 'Lighting'

settings = Settings()


def get_window_center(width=None, height=None):
    width = width or glut.get_window_width()
    height = height or glut.get_window_height()
    x = glut.get_screen_width() - width
    y = glut.get_screen_height() - height
    return x >> 1, y >> 1


def display_callback():
    gl.clear_color(PINK_COLOR)
    gl.clear(gl.Buffer.COLOR_BUFFER_BIT, gl.Buffer.DEPTH_BUFFER_BIT)
    gl.load_identity()

    x_eye = settings.sphere_center[0] + settings.view_radius * sin(settings.view_theta) * cos(settings.view_phi)
    z_eye = settings.sphere_center[0] + settings.view_radius * sin(settings.view_theta) * sin(settings.view_phi)
    y_eye = settings.sphere_center[0] + settings.view_radius * cos(settings.view_theta)

    glu.look_at(x_eye, y_eye, z_eye, *settings.sphere_center)

    draw_fog()
    draw_animation()
    draw_spiral()

    gl.flush()

    gl.disable(gl.Capability.LIGHT0)
    gl.disable(gl.Capability.LIGHT1)

    glut.swap_buffers()


def draw_fog():
    if not settings.fog_enabled:
        gl.fog(gl.FogParam.FOG_DENSITY, 0.0)
        return
    gl.fog(gl.FogParam.FOG_DENSITY, 0.5)
    gl.fog(gl.FogParam.FOG_COLOR, settings.fog_color)
    gl.fog_mode(gl.FogParam.FOG_MODE, gl.FogMode.EXP2)
    gl.fog(gl.FogParam.FOG_START, -0.3)
    gl.fog(gl.FogParam.FOG_END, 0.3)
    gl.hint(gl.FogParam.FOG_HINT, gl.FogParam.NICEST)


def draw_spiral():
    gl.push_matrix()
    gl.rotate(settings.spiral_z_deg, 0, 0, 1)
    gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.spiral_material)
    if settings.spiral_display_list is None:
        settings.spiral_display_list = gl.gen_lists(1)
        gl.new_list(settings.spiral_display_list, gl.ListMode.COMPILE)
        k = 9.5
        alpha, beta = 0.01, 0.0006
        gamma = 1. + beta
        sigma = -0.8
        gl.begin(gl.BeginMode.LINE_STRIP)
        for theta in np.linspace(0., 2 * pi * k, int(2 * k) * 360):
            beta *= gamma
            r = alpha + beta * theta
            x = r * cos(theta)
            y = r * sin(theta)
            gl.vertex3(x, y, sigma * sqrt(x ** 2 + y ** 2))
        gl.end()
        gl.end_list()
    gl.call_list(settings.spiral_display_list)
    gl.pop_matrix()


def draw_animation():
    gl.light_model(gl.LightModel.LIGHT_MODEL_AMBIENT, settings.light_ambient)
    if settings.projection_enabled:
        gl.enable(gl.Capability.LIGHT1)

        gl.light(gl.Capability.LIGHT1, gl.LightParameter.DIFFUSE, settings.projection_light_diffuse)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.POSITION, settings.projection_light_position)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_CUTOFF, settings.projection_light_spot_cutoff)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_DIRECTION, settings.projection_light_spot_direction)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.SPOT_EXPONENT, settings.projection_light_spot_exponent)

        gl.light(gl.Capability.LIGHT1, gl.LightParameter.CONSTANT_ATTENUATION,
                 settings.point_light_constant_attenuation)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.LINEAR_ATTENUATION, settings.point_light_linear_attenuation)
        gl.light(gl.Capability.LIGHT1, gl.LightParameter.QUADRATIC_ATTENUATION,
                 settings.point_light_quadratic_attenuation)
    else:
        gl.enable(gl.Capability.LIGHT0)

        gl.light(gl.Capability.LIGHT0, gl.LightParameter.DIFFUSE, settings.point_light_diffuse)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.POSITION, settings.point_light_position)

        gl.light(gl.Capability.LIGHT0, gl.LightParameter.CONSTANT_ATTENUATION,
                 settings.point_light_constant_attenuation)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.LINEAR_ATTENUATION, settings.point_light_linear_attenuation)
        gl.light(gl.Capability.LIGHT0, gl.LightParameter.QUADRATIC_ATTENUATION,
                 settings.point_light_quadratic_attenuation)
    if settings.sphere_radius >= settings.sphere_min_radius:
        gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.sphere_material)
        glut.solid_sphere(*settings.sphere_solid_parameters)
    gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.wall_material)
    min_edge = -settings.wall_size / 2
    max_edge = -min_edge
    if settings.wall_display_list is None:
        settings.wall_display_list = gl.gen_lists(1)
        gl.new_list(settings.wall_display_list, gl.ListMode.COMPILE)

        gl.begin(gl.BeginMode.QUADS)

        for wall_x in np.arange(min_edge, max_edge, settings.wall_step):
            for wall_y in np.arange(min_edge, max_edge, settings.wall_step):
                gl.vertex3(wall_x, wall_y, settings.wall_z)
                gl.vertex3(wall_x, wall_y + settings.wall_step, settings.wall_z)
                gl.vertex3(wall_x + settings.wall_step, wall_y + settings.wall_step, settings.wall_z)
                gl.vertex3(wall_x + settings.wall_step, wall_y, settings.wall_z)

        gl.end()

        gl.end_list()

    gl.begin(gl.BeginMode.QUADS)
    gl.vertex3(min_edge, max_edge, -settings.wall_z)
    gl.vertex3(min_edge, max_edge, settings.wall_z)
    gl.vertex3(min_edge, min_edge, settings.wall_z)
    gl.vertex3(min_edge, min_edge, -settings.wall_z)
    gl.end()

    def collision(particle: Particle):
        x, y, z = particle.position
        if z > settings.wall_z and (min_edge <= x <= max_edge) and (min_edge <= y <= max_edge):
            particle.position[2] = settings.wall_z
            particle.velocity[2] *= -1
        elif x < min_edge and (min_edge <= y <= max_edge) and (-settings.wall_z <= z <= settings.wall_z):
            particle.position[0] = min_edge
            particle.velocity[0] *= -1

    gl.call_list(settings.wall_display_list)

    gl.material(gl.MaterialFace.FRONT_AND_BACK, gl.MaterialParameter.AMBIENT_AND_DIFFUSE, settings.sphere_material)
    if settings.update_particles:
        settings.explosion.update(settings.time, collision)
    else:
        gl.call_list(settings.explosion.display_list)


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
    elif key == b'\'':
        settings.view_theta += settings.view_delta_rad
    elif key == b'\\':
        settings.view_theta -= settings.view_delta_rad
    elif key == b' ':
        settings.projection_enabled = not settings.projection_enabled
    elif key == b'-':
        settings.view_radius += 0.25
    elif key == b'=':
        settings.view_radius -= 0.25
    elif key == b'9':
        settings.light_intensity -= 0.1
    elif key == b'0':
        settings.light_intensity += 0.1
    elif key == b'.':
        settings.wall_detailing = 20
    elif key == b'p':
        settings.pause = not settings.pause
    elif key == b'u':
        settings.update_particles = not settings.update_particles
    elif key == b'f':
        settings.fog_enabled = not settings.fog_enabled
    glut.post_redisplay()


def idle_callback():
    if settings.pause:
        return
    settings.time += settings.delta_time
    settings.spiral_z_deg += settings.spiral_z_delta

    settings.sphere_radius -= settings.sphere_radius_delta
    if settings.sphere_radius < settings.sphere_min_radius:
        settings.explosion.explode(settings.time)

    glut.post_redisplay()


def init():
    print(bool(glutSetOption))


def main():
    glut.init(sys.argv)
    glut.init_display_mode(glut.DisplayMode.DEPTH, glut.DisplayMode.RGB, glut.DisplayMode.DOUBLE,
                           glut.DisplayMode.MULTISAMPLE,
                           )
    glut.init_window_size(*INITIAL_WINDOW_SIZE)
    glut.init_window_position(*get_window_center(*INITIAL_WINDOW_SIZE))
    glut.create_window(TITLE)

    gl.shade_model(gl.ShadingTechnique.SMOOTH)

    # gl.enable(gl.Capability.CULL_FACE)
    gl.enable(gl.Capability.DEPTH_TEST)
    gl.enable(gl.Capability.LIGHTING)
    gl.enable(gl.Capability.LINE_SMOOTH)
    gl.enable(gl.Capability.FOG)
    gl.enable(gl.Capability.MULTISAMPLE_ARB)  # AA

    gl.light_model(gl.LightModel.LIGHT_MODEL_TWO_SIDE, gl.Bool.TRUE)

    glut.display_func(display_callback)
    glut.reshape_func(reshape_callback)
    glut.keyboard_func(keyboard_callback)
    glut.idle_func(idle_callback)

    init()

    glut.main_loop()


if __name__ == '__main__':
    main()

# Системы частиц первого порядка	4
# Анимация объекта(-ов)	2
# Туман	2
# Антиалиасинг (сглаживание)	6
# Программно-заданный объект нетривиальной формы (с дырками)	6
# Слоистый туман	6
# Передвижение наблюдателя в пространстве и изменение угла обзора (обработка клавишей мыши и клавиатуры)	2

# 4 + 2 + 2 + 6 + 6 + 6 + 2
