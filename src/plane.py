from agent import Agent

class Plane(Agent):
	def __init__(self, name, x, y, dx, dy, model):
		Agent.__init__(self, name, x, y, model)

		self.dx = dx #momentum in x direction
		self.dy = dy #momentum in y direction

	def run_epoch(self):
		self.pos[0] += self.dx #use numpys vector addition
		self.pos[1] += self.dy
		print('xpos: %d, ypos: %d' % (self.pos[0], self.pos[1]))
