'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Handles the movement, existence and message sending of planes. 
					Superclass of Agent. 
'''
from agent import Agent
import random
class Plane(Agent):
	def __init__(self, name, x, y, dx, dy, isfriendly, model):
		Agent.__init__(self, name, x, y, model)
		self.dx = dx #momentum in x direction
		self.dy = dy #momentum in y direction
		self.isfriendly = isfriendly
		self.isdestroyed = False
		self.isvisible = True
		self.correct_identification = False
		self.reply = self.generate_reply()


	def generate_reply(self):
		if self.isfriendly and random.random() > 0.1:
			self.correct_identification = True
			return "friendly"
		else: 
			return "unknown"

	def run_epoch(self,message_manager):
		self.update(message_manager)
		self.pos[0] += self.dx
		self.pos[1] += self.dy
		if self.pos[1] == 10 or self.pos[1]  < 0 or self.pos[0] == 10 or self.pos[0] < 0:
			self.destroy()
		# print('xpos: %d, ypos: %d' % (self.pos[0], self.pos[1]))

		if "indentify" in self.knowledge:
			for (message, identifier, sender) in self.received_messages:
				if self.correct_identification and not "K_%s(friendly)" % sender.name in self.knowledge:
						self.send_new_message(sender,"friendly",message_manager)
				if not self.correct_identification and not "K_%s(unknown)" % sender.name in self.knowledge:
					self.send_new_message(sender, "unknown",message_manager)

	def destroy(self):
		print('plane crashed')
		if self in self.model.planes: 
			self.model.planes.remove(self)
		self.isdestroyed = True
		self.isvisible = False