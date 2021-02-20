import numpy as np
from localization import particle_filter
from navigation.parameters import *
from sensors.parameters import *

NUM_PARTICLES = 40
STD_V = 1.6
STD_Y = 0.3
STD_M = 0.2

# measurements = [(5.4, 0.4, 0.5, 0.6), (5.3, 0.5, 0.5, 0.6), (5.2, 0.6, 0.5, 0.6), (5.1, 0.7, 0.5, 0.6)]
# steerings = [(0.1, 0.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0)]


def read_data(filename):
    with open(filename) as file:
        data = np.loadtxt(file)
    return data


def main():
    pf = particle_filter.ParticleFilter(NUM_PARTICLES, True)
    pf.draw("Start")
    data = read_data("./data/logs/1613307394.txt")
    start_time = 1613307395027
    # for steering, measurement in zip(steerings, measurements):
    for line in data:
        timestamp = line[0]
        measurement = line[1:5] / 100
        dt = (timestamp - start_time) / 1000
        start_time = timestamp
        steering = line[5]
        if steering == 0:
            vel = VELOCITY
            yaw_rate = 0
        elif steering == 1:
            vel = 0
            yaw_rate = TURN_RATE
        elif steering == 2:
            vel = -VELOCITY
            yaw_rate = 0
        elif steering == 3:
            vel = 0
            yaw_rate = -TURN_RATE
        else:
            vel = 0
            yaw_rate = 0

        std_v = STD_V * abs(vel) + 0.1
        std_y = STD_Y * abs(yaw_rate) + 0.1
        print(timestamp, measurement, dt, vel, yaw_rate, std_v, std_y)
        pf.predict(dt, vel, yaw_rate, [std_v, std_y])
        best_index = pf.update(measurement, sensor_poses, STD_M)
        pf.resample()
        print("Best particle", best_index)
        pf.show(best_index)
        # pf.particles[best_index].print()


main()
