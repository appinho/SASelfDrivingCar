import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

MAP_X = 6.0
MAP_Y = 1.2
EDGE = 40
RES = 200
ARROW = 30
NUM_PARTICLES = 100
STD_V = 1.8
STD_Y = 1.8
STD_M = 0.2
RESAMPLING_RATE = 0.7
DRAW = False
COLORS = ['g', 'r', 'c', 'm', 'y']

def GET_COLOR(i):
	j = i % len(COLORS)
	return COLORS[j]

sensor_pose = [(0.1, 0.0, 0.0), (-0.1, 0.0, np.pi), (0.0, -0.05, np.pi/2), (0.0, 0.05, -np.pi / 2)]
measurements = [(5.4, 0.4, 0.5, 0.6), (5.3, 0.5, 0.5, 0.6), (5.2, 0.6, 0.5, 0.6), (5.1, 0.7, 0.5, 0.6)]
steerings = [(0.1, 0.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0), (0.1, 1.0, 0.0)]

class Particle():
	def __init__(self, i):
		self.i = i
		self.x = MAP_X * random.uniform(0,1)
		self.y = MAP_Y * random.uniform(0,1)
		self.o = 2 * np.pi * random.uniform(0,1)
		self.w = random.uniform(0,1)
		#self.print()
	def print(self):
		print("Particle %d at %f,%f with o=%f and w=%f" % (self.i, self.x, self.y, self.o, self.w))

class Landmark():
	def __init__(self, i, x, y, o):
		self.i = i
		self.x = x
		self.y = y
		self.o = o
	def print(self):
		print("Landmark %d at %f,%f with o=%f" % (self.i, self.x, self.y, self.o))

				
	def line_x_rectangle(self, x_min=0, y_min=0, x_max=MAP_X, y_max=MAP_Y):
		a = np.tan(self.o)
		b = self.y - a * self.x
		# Intersections of f(x) = ax + b with the rectangle. (x, y, axis)
		p1, p2 = (x_min, a * x_min + b, 'x'), (x_max, a * x_max + b, 'x'), 
		p3, p4 = ((y_min - b) / a, y_min, 'y'), ((y_max - b) / a, y_max, 'y')
		# Python sorts them using the first key
		p1, p2, p3, p4 = sorted([p1, p2, p3, p4])

		# Check if there is an intersection, returns the points otherwise
		if p1[2] == p2[2]:
			return None
		return p2[:2], p3[:2]
		
	def get_min_distance2(self):
		points = self.line_x_rectangle()
		if points is None:
			return 100.0
		dx0 = points[0][0] - self.x
		dy0 = points[0][1] - self.y
		dx1 = points[1][0] - self.x
		dy1 = points[1][1] - self.y
		d0 = np.sqrt(dx0*dx0+dy0*dy0)
		d1 = np.sqrt(dx1*dx1+dy1*dy1)
		d = min(d0, d1)
		#print(d)
		return d
class ParticleFilter():
	def __init__(self, num_particles):
		self.num_particles = num_particles
		#self.weights = []
		self.cumulated_weights = []
		self.particles = []
		for i in range(self.num_particles):
			self.init(i)
		self.landmarks = []
	
	def init(self, index):
		self.particles.append(Particle(index))
	def predict(self, steering, std_pos):
		self.landmarks = []
		dt = steering[0]
		vel = steering[1]
		yaw_rate = steering[2]
		for particle in self.particles:
			n_vel = np.random.normal(vel, std_pos[0])
			n_yaw_rate = np.random.normal(yaw_rate, std_pos[1])
			particle.o += n_yaw_rate * dt
			
			if np.abs(n_yaw_rate) > 0.001:
				particle.x += n_vel / n_yaw_rate * (np.sin(particle.o + n_yaw_rate * dt) - np.sin(particle.o))
				particle.y += n_vel / n_yaw_rate * (np.cos(particle.o) - np.cos(particle.o + n_yaw_rate * dt))
			else:
				particle.x += n_vel * dt * np.cos(particle.o)
				particle.y += n_vel * dt * np.sin(particle.o)
			#particle.print()
	def update(self, measurement):
		self.sum_w = 0.0
		max_w = 0.0
		best_index = -1
		for i, p in enumerate(self.particles):
			w = 1.0
			for j, m in enumerate(measurement):
				x = p.x + sensor_pose[j][0]
				y = p.y + sensor_pose[j][1]
				o = p.o + sensor_pose[j][2]
				#print("L", x,y,o)
				x_new = x + np.cos(o) * m
				y_new = y + np.sin(o) * m
				#print(x_new, y_new)
				l = Landmark(p.i, x_new, y_new, o)
				#l.print()
				self.landmarks.append(l)
				min_distance = l.get_min_distance2()
				#result = l.line_x_rectangle()
				#print('D', min_distance)
				w *= 1 / np.sqrt(2 * np.pi * STD_M * STD_M) * np.exp(-1/2*(min_distance/STD_M)**2)
				#print(w)
			p.w = w
			if(w > max_w):
				best_index = i
				max_w = w
			self.sum_w += w
		self.draw()
		self.cumulated_weights = [0.0]
		for p in self.particles:
			p.w /= self.sum_w
			self.cumulated_weights.append(self.cumulated_weights[-1] + p.w)
		#print("CUM W", self.cumulated_weights)
		return best_index
				
	def resample(self):
		new_particles = []
		num_resamples = int(RESAMPLING_RATE * self.num_particles)
		for i in range(num_resamples):
			r = random.uniform(0,1)
			index = self.num_particles
			for j in range(self.num_particles):
				if r > self.cumulated_weights[j] and r <= self.cumulated_weights[j+1]:
					index = j
					break
			new_particle = copy.deepcopy(self.particles[index])
			new_particle.i = i
			#new_particle.print()
			new_particles.append(new_particle)
		self.particles = new_particles
		for i in range(num_resamples, self.num_particles):
			self.init(i)
			
	def draw(self, best_index=-1, draw=False):
		if not DRAW and not draw:
			return
		fig, ax = plt.subplots(1)
		ax.set_xlim([-EDGE*MAP_X, EDGE*MAP_X + RES*MAP_X])
		ax.set_ylim([-EDGE*MAP_Y, EDGE*MAP_Y + RES*MAP_Y])
		rect = patches.Rectangle((0,0), RES*MAP_X, RES*MAP_Y, linewidth=1, edgecolor='k', facecolor = 'none')
		ax.add_patch(rect)
		for p in self.particles:
			if p.i != best_index:
				continue
			#p.print()
			x_2 = np.cos(p.o) * ARROW
			y_2 = np.sin(p.o) * ARROW
			x_s = p.x*RES
			y_s = p.y*RES
			x_e = x_2
			y_e = y_2
			#c = GET_COLOR(p.i)
			c = 'k'
			ax.arrow(x_s, y_s, x_e, y_e, head_width=10, head_length=10, fc=c, ec=c)
		for l in self.landmarks:
			if l.i != best_index:
				continue
			#c = GET_COLOR(l.i)
			c = 'k'
			ax.plot(l.x*RES, l.y*RES, c+'o')
		plt.show()
		

			
def main():
	pf = ParticleFilter(NUM_PARTICLES)
	pf.draw()
	
	for steering, measurement in zip(steerings, measurements):
		pf.predict(steering, [STD_V, STD_Y])
		pf.draw()
		best_index = pf.update(measurement)
		pf.resample()
		print("Best particle", best_index)
		pf.particles[best_index].print()
		pf.draw(best_index, draw=True)
main()
