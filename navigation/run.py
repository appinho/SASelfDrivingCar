from navigation import steering
from navigation import parameters
import time

DELAY = 0.01
class Drive():
	def __init__(self):
		self.path = [
			(2.0*parameters.TTT_1M, 0),
			(parameters.TTT_90DEG, 1),
			(1.0*parameters.TTT_1M, 0),
			(parameters.TTT_90DEG, 1),
			(4.0*parameters.TTT_1M, 0),
			(parameters.TTT_90DEG, 1),
			(1.0*parameters.TTT_1M, 0),
			(parameters.TTT_90DEG, 1),
			(2.0*parameters.TTT_1M, 0),
			(0.2, -1)
		]
		self.path_index = 0		
		self.before = round(time.time() * 1000)
	def run(self, now):
		duration = (now - self.before) / 1000.0
		steering.init()
		if duration < self.path[self.path_index][0]:
			self.steer(self.path[self.path_index][1])
		else:
			self.path_index +=1
			if self.path_index >= len(self.path):
				return True
			self.steer(self.path[self.path_index][1])
			self.before = now
		return False
	def steer(self, index):
		if index == 0:
			steering.forward(DELAY)
		elif index == 1:
			steering.turn_left(DELAY)
		elif index == 2:
			steering.reverse(DELAY)
		elif index == 3:
			steering.turn_right(DELAY)
		else:
			steering.stop(DELAY)
