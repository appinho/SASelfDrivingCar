import numpy as np
from localization import particle_filter
from localization import viz
from navigation.parameters import *
from sensors.parameters import *

# log_file = "1613307394.txt"
log_file = "1613900096.txt"

DRAW = True
SAVE = False
START = 0


def read_data(filename):
    with open(filename) as file:
        data = np.loadtxt(file)
    return data


def main():
    log_filename = "./data/logs/" + log_file
    data = read_data(log_filename)
    start_time = int(data[START][0])
    start_x = data[START][3] / 100 + 0.1425
    start_y = data[START][4] / 100 + 0.09
    start_o = 0.0
    pf = particle_filter.ParticleFilter(x=start_x, y=start_y, o=start_o)
    # viz.draw("Start", pf.particles, pf.i, save=SAVE, draw=DRAW)
    # for steering, measurement in zip(steerings, measurements):
    for i, line in enumerate(data[START:]):
        steering = line[5]
        sensor_data = [line[0], line[1:5]]
        best_index = pf.run(
            steering,
            sensor_data,
            sensor_poses,
            VELOCITY,
            TURN_RATE)
        if not best_index:
            continue
        bp = pf.particles[best_index]
        if not bp:
            continue
        title = "t=%d x=%.2f y=%.2f o=%.2f" % (i, bp.x, bp.y, bp.o)
        print(title)
        viz.draw(
            title,
            pf.particles,
            i,
            best_index=best_index,
            save=SAVE,
            draw=DRAW,
        )
        pf.resample()
        pf.show(best_index)
        # pf.particles[best_index].print()


main()
