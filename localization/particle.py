from maps import *
import random
import numpy as np

class Particle():
	def __init__(self, i):
		self.i = i
		self.x = MAP_X * random.uniform(0,1)
		self.y = MAP_Y * random.uniform(0,1)
		self.o = 2 * np.pi * random.uniform(0,1)
		self.w = random.uniform(0,1)

	def show(self):
		print("Particle %d at %f,%f with o=%f and w=%f" % (self.i, self.x, self.y, self.o, self.w))
