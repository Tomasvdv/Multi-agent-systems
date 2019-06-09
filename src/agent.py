'''
Code written by: 	Steff Groefsema, Tomas van der Velde and Ruben Cöp
Description:		Agent is a subclass of the turret and plane classes. It handles basic functionality 
					of these agents like the communication between them and updating of knowledge.
'''

import random
import numpy as np

class Agent:
	def __init__(self, name, x, y, model):
		self.FAIL_PROB = 0.2	
		self.knowledge = set([]) #sets can't contain duplicates.
		self.sent_messages = []
		self.received_messages = []
		self.agents = []		#connected agents
		self.name = str(name)
		self.messageidx = 0
		self.confirmed = {} #dict of identifiers of all messages sent
		self.kripke_knowledge = {} #dict of knowledge that is used to construct Kripke model

		self.x = x
		self.y = y

		self.pos = np.array((x, y))

		self.model = model

	def broadcast(self, message,message_manager):
		#send message to all connected agents
		for a in self.agents:
			self.send_new_message(a, message,message_manager)

	def update(self, message_manager):
		#resend possibly failed messages
		resent_this_epoch = False
		for (message, identifier, other) in self.sent_messages:
			if self.name in identifier and self.confirmed[identifier] != 1: #not yet confirmed
				self.resend_last_message(identifier,message_manager)
				resent_this_epoch = True

		return resent_this_epoch

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

	def send_new_message(self, other, message,message_manager):
		identifier = str(self.messageidx) + self.name
		#print("%s sent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier))
		self.sent_messages.append((message, identifier, other))
		other.receive_message(self, message, identifier,message_manager)
		self.confirmed[identifier] = 0
		self.messageidx += 1

	def resend_last_message(self, identifier,message_manager):
		for idx in range(len(self.sent_messages)-1, -1, -1): #loop from last message to first
			(message, midentifier, other) = self.sent_messages[idx]
			if midentifier == identifier:
				if (other.name is message_manager.tracked) or (self.name is message_manager.tracked):
					message_manager.add_message(str("%s resent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier)))
				#print("%s resent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier))
				other.receive_message(self, message, identifier,message_manager)
				return
		# print("could not find message", idx)
		# print(self.sent_messages)

	def receive_message(self, other, message, identifier,message_manager):
		successfully_received = random.random() > self.FAIL_PROB
		if successfully_received:
			self.knowledge.add(message)
			self.received_messages.append((message, identifier, other))
			if (other.name is message_manager.tracked) or (self.name is message_manager.tracked):
				message_manager.add_message(str("%s successfully received a message! \"%s\"" % (self.name, message)))
			# print("%s successfully received a message! \"%s\"" % (self.name, message))
			self.send_reply(other, message, identifier,message_manager)

			

	def send_reply(self, other, message, identifier,message_manager):
		reply = "K_%s(%s)"  % (self.name, message)

		self.knowledge.add(reply) #add the reply to knowledge base

		if reply.count("K_%s" % self.name) >= 2 and reply.count("K_") == 4: #e.g. K_a(K_b(K_a(K_b(1))))
			self.confirmed[identifier] = 1
		else:
			self.sent_messages.append((reply, identifier, other))
			if (other.name is message_manager.tracked) or (self.name is message_manager.tracked):
				message_manager.add_message(str("%s sent a reply to %s. \"%s\" (%s)" % (self.name, other.name, reply, identifier))) 
			#print("%s sent a reply to %s. \"%s\" (%s)" % (self.name, other.name, reply, identifier))
			other.receive_message(self, reply, identifier,message_manager)


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