import random
import numpy as np

from localization.landmark import Landmark
from localization.maps import MAP_X, MAP_Y


class Particle:
    def __init__(self, i, x=None, y=None, o=None):
        self.i = i
        if x:
            self.x = x
        else:
            self.x = MAP_X * random.uniform(0, 1)
        if y:
            self.y = y
        else:
            self.y = MAP_Y * random.uniform(0, 1)
        if o:
            self.o = o
        else:
            self.o = 2 * np.pi * random.uniform(0, 1)
        self.w = random.uniform(0, 1)
        self.landmarks = []

    def show(self):
        print(
            "Particle %d at %f,%f with o=%f and w=%f"
            % (self.i, self.x, self.y, self.o, self.w)
        )
