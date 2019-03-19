from math import radians, pi

import numpy as np

from graphics import GlColor, gl, glut

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


class Particle(object):
    def __init__(self, position=None,
                 velocity=None,
                 acceleration=None,
                 gravitation=None,
                 attenuation=0.0,
                 initial_time=0.0):
        self.position = position or [0., 0., 0.]
        self.velocity = velocity or [0., 0., 0.]
        self.acceleration = acceleration or [0., 0., 0.]
        self.attenuation = attenuation
        self.gravitation = gravitation or [0., 0., 0.]
        self.time = initial_time

    def update(self, time):
        t = time - self.time
        self.time = time

        acceleration = [a + g for a, g in zip(self.acceleration, self.gravitation)]
        self.position = [x + v * t + 0.5 * a * t ** 2 for x, v, a in
                         zip(self.position, self.velocity, acceleration)]
        self.velocity = [v + a * t for v, a in zip(self.velocity, acceleration)]
        self.acceleration = [a - a * self.attenuation for a in self.acceleration]


class Explosion(object):
    def __init__(self, position, power, particle_count=100, particle_size=1.0, seed=None):
        self.power = power
        self.position = position
        self.particle_size = particle_size
        self.particle_count = particle_count
        self.particles = []  # type: list[Particle]
        self.random_state = np.random.RandomState(seed=seed)
        self.exploded = False
        self.display_list = None

    def explode(self, time):
        if self.exploded:
            return

        for i in range(self.particle_count):
            direction = [np.random.uniform(-1, 1) for _ in range(3)]
            power = np.random.uniform(0.05 * self.power, self.power)
            acceleration = [d * power for d in direction]
            self.particles.append(Particle(
                self.position,
                acceleration=acceleration,
                attenuation=0.3,
                initial_time=time,
            ))

        self.display_list = gl.gen_lists(1)
        gl.new_list(self.display_list, gl.ListMode.COMPILE)
        glut.solid_sphere(0.5, 500, 500)
        gl.end_list()

        self.exploded = True

    def update(self, time, collision_f=None):
        if not self.exploded:
            return
        for i in range(self.particle_count):
            self.particles[i].update(time)
            gl.push_matrix()
            gl.translate(*self.particles[i].position)
            gl.scale(self.particle_size, self.particle_size, self.particle_size)
            gl.call_list(self.display_list)
            gl.pop_matrix()

            if collision_f is not None:
                collision_f(self.particles[i])


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

    projection_enabled = False

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

    sphere_material = [*BLUE_COLOR.to_float(), 1.0]
    sphere_initial_radius = 0.2
    sphere_min_radius = sphere_initial_radius / 20
    sphere_radius = sphere_initial_radius
    sphere_radius_delta = sphere_initial_radius / 50
    sphere_detailing = 500

    wall_material = [*SMOKE_COLOR.to_float(), 1.0]
    wall_z = 0.8
    wall_size = 2
    wall_detailing = 140

    wall_display_list = None

    explosion_power = 100
    explosion = Explosion([0, 0, 0], explosion_power, 200, sphere_initial_radius / 10, 0)

    time = 0.
    delta_time = 0.01

    @property
    def light_ambient(self):
        return [self.light_intensity, self.light_intensity, self.light_intensity, 1]

    @property
    def sphere_solid_parameters(self):
        return [self.sphere_radius, self.sphere_detailing, self.sphere_detailing]

    @property
    def wall_step(self):
        return 1 / self.wall_detailing
