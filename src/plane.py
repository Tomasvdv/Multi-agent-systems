from agent import Agent

class Plane(Agent):
	def __init__(self, name, x, y, dx, dy, isfriendly, model):
		Agent.__init__(self, name, x, y, model)

		self.dx = dx #momentum in x direction
		self.dy = dy #momentum in y direction
		self.isfriendly = isfriendly
		self.isdestroyed = False
		self.isvisible = True

	def run_epoch(self):
		self.pos[0] += self.dx
		self.pos[1] += self.dy
		print('xpos: %d, ypos: %d' % (self.pos[0], self.pos[1]))

		if "indentify" in self.knowledge:
			for (message, identifier, sender) in self.received_messages:
				if self.isfriendly and not "K_%s(friendly)" % sender.name in self.knowledge:
					self.send_new_message(sender, "friendly")
				if not self.isfriendly and not "K_%s(not_friendly)" % sender.name in self.knowledge:
					self.send_new_message(sender, "not_friendly")

	def destroy(self):
		if self in self.model.planes: 
			self.model.planes.remove(self)
		self.isdestroyed = True
		self.isvisible = False