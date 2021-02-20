from maps import *
import random
import numpy as np


class Particle:
    def __init__(self, i, x, y, o):
        self.i = i
        self.x = x  # MAP_X * random.uniform(0,1)
        self.y = y  # MAP_Y * random.uniform(0,1)
        self.o = o  # 0.0 * np.pi * random.uniform(0,1)
        self.w = random.uniform(0, 1)
        # self.show()

    def show(self):
        print(
            "Particle %d at %f,%f with o=%f and w=%f"
            % (self.i, self.x, self.y, self.o, self.w)
        )
