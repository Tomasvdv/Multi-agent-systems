'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Agent is a subclass of the turret and plane classes. It handles basic functionality 
					of these agents like the communication between them and updating of knowledge.
'''

import random
import numpy as np

class Agent:
	def __init__(self, name, x, y, model):
		self.knowledge = set([]) #sets can't contain duplicates.
		self.sent_messages = []
		self.received_messages = []
		self.agents = []		#connected agents
		self.name = str(name)
		self.messageidx = 0
		self.confirmed = {} #dict of identifiers of all messages sent
		self.kripke_knowledge = {} #dict of knowledge that is used to construct Kripke model
		self.counter = 0 ## used for counting the number of messages sent to plane
		self.x = x
		self.y = y
		self.isdestroyed = False
		self.isvisible = True

		self.inbox = [] ## used for saving messages
		self.pos = np.array((x, y))

		self.model = model

	def empty_messages(self):
		self.inbox = []
		self.sent_messages = []
		self.received_messages = []
		self.confirmed = {}
		self.counter = 0
		self.messageidx = 0

	def clean_up_messages(self,agent1):
		self.received_messages = [(m, i, s) for (m, i, s) in self.received_messages if s is not agent1]
		

	def broadcast(self, message):
		#send message to all connected agents
		for a in self.agents:
			self.send_new_message(a, message)

	def update(self):
		self.model.message_sender.check_inbox(self)

		#resend possibly failed messages
		for (key, val) in self.confirmed.items():
			print( "%s: %s %s " % (self.name, key, val))
			if val == 0: ## message not received
				self.resend_last_message(key)


	def to_model(self):
		main_knowledge = min(self.knowledge, key=len) #Take shortest knowledge element for now, for simplicity
		if (main_knowledge == 'friendly') or (main_knowledge == 'not_friendly'):
			self.kripke_knowledge[self.name] = [main_knowledge]
		else: #The turret is still in doubt about the status of the plane, so add both possibilities
			self.kripke_knowledge[self.name] = ['friendly', 'not_friendly']

	def printKB(self):
		print("KB of agent ",self.name)
		for k in self.knowledge:
			print("\t", k)

	def send_new_message(self, other, message):
		self.model.message_sender.send_message(self, other, message)

	def resend_last_message(self, identifier):
		self.model.message_sender.resend_message(self, identifier)
	
	def send_reply(self, other, message, identifier):
		self.model.message_sender.reply(self, other, message, identifier)

	def update_message_manager(self, other, message, identifier, messagetype):
		if (other.name is self.model.message_manager.tracked) or (self.name is self.model.message_manager.tracked):
			self.counter += 1 ## why?
			if messagetype == 'reply':
				self.model.message_manager.add_message(str("%s sent a reply to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier))) 
			elif messagetype == 'send':
				self.model.message_manager.add_message(str("%s sent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier)))
			elif messagetype == 'resend':
				self.model.message_manager.add_message(str("%s resent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier)))
			elif messagetype == 'receive':
				self.model.message_manager.add_message(str("%s successfully received a message! \"%s\"" % (self.name, message)))

	
if __name__ == '__main__':
	A = Agent("A", 0, 1, None)
	B = Agent("B", 0, 0, None)
	C = Agent("C", 1, 0, None)
	D = Agent("D", 1, 1, None)

	A.agents = [B, C, D]
	B.agents = [A, C, D]

	agents = [A, B, C, D]

	messages_A = ['hello'] #['hello', 'spam', 'message', 'bye']
	messages_B = ['hi'] #['hi', 'spam2', 'empty', 'goodbye']


	for message in messages_A:
		A.broadcast(message)

	for message in messages_A:
		B.broadcast(message)



	running = True
	while running:
		running = False
		if A.update():
			running = True
		if B.update():
			running = True

	print("---Final KB---")
	for a in agents:
		a.printKB()