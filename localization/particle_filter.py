import copy
import numpy as np
import random

from particle import Particle
from landmark import Landmark
from maps import *

RESAMPLING_RATE = 1.0
EDGE = 50
RES = 200
ARROW = 30
COLORS = ["g", "r", "c", "m", "y"]


def GET_COLOR(i):
    j = i % len(COLORS)
    return COLORS[j]


class ParticleFilter:
    def __init__(
        self,
        num_particles=40,
        x=0.4,
        y=1.35,
        o=0,
        std_v=1.6,
        std_y=0.3,
        std_m=0.2,
        save=False,
    ):
        self.num_particles = num_particles
        self.particles = []
        for i in range(self.num_particles):
            self.init(i, x, y, o)
        self.std_v = std_v
        self.std_y = std_y
        self.std_m = std_m
        self.cumulated_weights = []
        self.landmarks = []
        self.i = 0
        self.save = save
        self.best_index = -1
        self.t = 0

    def run(self, key, sensor_data, sensor_poses, VELOCITY, TURN_RATE):
        if len(sensor_data):
            timestamp = sensor_data[0]
            if self.t == 0:
                self.t = timestamp
                return
	    
            measurement = [x / 100 for x in sensor_data[1]]
            dt = (timestamp - self.t) / 1000
            if key == 0:
                vel = VELOCITY
                yaw_rate = 0
            elif key == 1:
                vel = 0
                yaw_rate = TURN_RATE
            elif key == 2:
                vel = -VELOCITY
                yaw_rate = 0
            elif key == 3:
                vel = 0
                yaw_rate = -TURN_RATE
            else:
                vel = 0
                yaw_rate = 0

            self.predict(dt, vel, yaw_rate)
            best_index = self.update(measurement, sensor_poses)
            self.resample()
            self.show(best_index)
            self.t = timestamp

    def get_standard_deviation(self, vel, yaw_rate):
	std_v = self.std_v * abs(vel) + 0.1
	std_y = self.std_y * abs(yaw_rate) + 0.1
	return [std_v, std_y]

    def show(self, index):
        self.particles[index].show()

    def init(self, index, x, y, o):
        self.particles.append(Particle(index, x, y, o))

    def predict(self, dt, vel, yaw_rate):
        self.landmarks = []
        [std_v, std_y] = self.get_standard_deviation(vel, yaw_rate)
        for particle in self.particles:
            n_vel = np.random.normal(vel, std_v)
            n_yaw_rate = np.random.normal(yaw_rate, std_y)
            particle.o += n_yaw_rate * dt

            if np.abs(n_yaw_rate) > 0.001:
                dx = (
                    n_vel
                    / n_yaw_rate
                    * (
                        np.sin(particle.o + n_yaw_rate * dt)
                        - np.sin(particle.o)
                    )
                )
                dy = (
                    n_vel
                    / n_yaw_rate
                    * (
                        np.cos(particle.o)
                        - np.cos(particle.o + n_yaw_rate * dt)
                    )
                )
            else:
                dx = n_vel * dt * np.cos(particle.o)
                dy = n_vel * dt * np.sin(particle.o)
            # print(dx, dy)
            particle.x += dx
            particle.y += dy
        # self.draw("Predict")

    def update(self, measurement, sensor_poses):
        self.sum_w = 0.0
        max_w = 0.0
        best_index = -1
        for i, p in enumerate(self.particles):
            # print("i", i)
            w = 1.0
            for j, m in enumerate(measurement):
                x = p.x + sensor_poses[j][0]
                y = p.y + sensor_poses[j][1]
                o = p.o + sensor_poses[j][2]
                # print("L", x,y,o)
                x_new = x + np.cos(o) * m
                y_new = y + np.sin(o) * m
                # print("NEW", x,y, o, m, x_new, y_new)
                l = Landmark(p.i, x_new, y_new, o)
                # l.show()
                self.landmarks.append(l)
                min_distance = l.get_min_distance2()
                # result = l.line_x_rectangle()
                # print('D', min_distance)
                w *= (
                    1
                    / np.sqrt(2 * np.pi * self.std_m * self.std_m)
                    * np.exp(-1 / 2 * (min_distance / self.std_m) ** 2)
                )
                # print(min_distance, w)
                # print(w)
            if w < 0.00001:
                w = 0.00001
            p.w = w
            if w > max_w:
                best_index = i
                max_w = w
            self.sum_w += w
        # self.draw()
        self.cumulated_weights = [0.0]
        for p in self.particles:
            p.w /= self.sum_w
            self.cumulated_weights.append(self.cumulated_weights[-1] + p.w)
        # self.draw("Update", best_index, True)
        # print(self.cumulated_weights)
        self.best_index = best_index
        return best_index

    def resample(self):
        new_particles = []
        num_resamples = int(RESAMPLING_RATE * self.num_particles)
        for i in range(num_resamples):
            r = random.uniform(0, 1)
            index = self.num_particles
            for j in range(self.num_particles):
                if (
                    r > self.cumulated_weights[j]
                    and r <= self.cumulated_weights[j + 1]
                ):
                    index = j
                    break
            new_particle = copy.deepcopy(self.particles[index])
            new_particle.i = i
            # new_particle.print()
            new_particles.append(new_particle)
        self.particles = new_particles
        for i in range(num_resamples, self.num_particles):
            self.init(i)
        # self.draw("Resample")
        self.i += 1
