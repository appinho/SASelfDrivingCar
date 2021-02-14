import copy
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from particle import Particle
from landmark import Landmark
from maps import *

STD_M = 0.2
RESAMPLING_RATE = 0.7


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
	def update(self, measurement, sensor_poses):
		self.sum_w = 0.0
		max_w = 0.0
		best_index = -1
		for i, p in enumerate(self.particles):
			w = 1.0
			for j, m in enumerate(measurement):
				x = p.x + sensor_poses[j][0]
				y = p.y + sensor_poses[j][1]
				o = p.o + sensor_poses[j][2]
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
		if not draw:
			return
		print("S")
		
		fig, ax = plt.subplots(1)
		"""
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
		"""
