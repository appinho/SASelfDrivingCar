import numpy as np
from particle_filter import ParticleFilter

EDGE = 40
RES = 200
ARROW = 30
DRAW = False
COLORS = ['g', 'r', 'c', 'm', 'y']

NUM_PARTICLES = 100
STD_V = 1.8
STD_Y = 1.8

def GET_COLOR(i):
	j = i % len(COLORS)
	return COLORS[j]

sensor_poses = [(0.1, 0.0, 0.0), (-0.1, 0.0, np.pi), (0.0, -0.05, np.pi/2), (0.0, 0.05, -np.pi / 2)]
measurements = [(5.4, 0.4, 0.5, 0.6), (5.3, 0.5, 0.5, 0.6), (5.2, 0.6, 0.5, 0.6), (5.1, 0.7, 0.5, 0.6)]
steerings = [(0.1, 0.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0)]

def main():
	pf = ParticleFilter(NUM_PARTICLES)
	pf.draw()
	
	for steering, measurement in zip(steerings, measurements):
		pf.predict(steering, [STD_V, STD_Y])
		pf.draw()
		best_index = pf.update(measurement, sensor_poses)
		pf.resample()
		print("Best particle", best_index)
		#pf.particles[best_index].print()
		pf.draw(best_index, draw=True)
main()