import random
import numpy as np

class Agent:
	def __init__(self, name):
		self.FAIL_PROB = 0.9	
		self.knowledge = set([]) #sets can't contain duplicates.
		self.sent_messages = [] 
		self.received_messages = []

		self.agents = []		#connected agents
		self.name = str(name)
		self.messageidx = 0
		self.confirmed = {} #dict of identifiers of all messages sent

	def broadcast(self, message):
		#send message to all connected agents
		for a in self.agents:
			self.send_new_message(a, message)

	def update(self):
		#resend possibly failed messages
		resent_this_epoch = False
		for (message, identifier, other) in self.sent_messages:
			if self.name in identifier and self.confirmed[identifier] != 1: #not yet confirmed
				self.resend_last_message(identifier)
				resent_this_epoch = True

		return resent_this_epoch

	def get_KB(self):
		#return knowledge base in some format.
		return self.knowledge

	def send_new_message(self, other, message):
		identifier = str(self.messageidx) + self.name
		print("%s sent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier))
		self.sent_messages.append((message, identifier, other))
		other.receive_message(self, message, identifier)
		self.confirmed[identifier] = 0
		self.messageidx += 1

	def resend_last_message(self, identifier):
		for idx in range(len(self.sent_messages)-1, -1, -1): #loop from last message to first
			(message, midentifier, other) = self.sent_messages[idx]
			if midentifier == identifier:
				print("%s resent a message to %s. \"%s\" (%s)" % (self.name, other.name, message, identifier))
				other.receive_message(self, message, identifier)
				return
		# print("could not find message", idx)
		# print(self.sent_messages)

	def receive_message(self, other, message, identifier):
		successfully_received = random.random() > self.FAIL_PROB
		if successfully_received:
			self.knowledge.add(message)
			self.received_messages.append((message, identifier, other))
			print("%s successfully received a message! \"%s\"" % (self.name, message))
			self.send_reply(other, message, identifier)

			

	def send_reply(self, other, message, identifier):
		reply = "K_%s(%s)"  % (self.name, message)

		self.knowledge.add(reply) #add the reply to knowledge base

		if reply.count("K_%s" % self.name) == 2 and reply.count("K") == 4: #e.g. K_a(K_b(K_a(K_b(1))))
			self.confirmed[identifier] = 1
		else:
			self.sent_messages.append((reply, identifier, other))
			print("%s resent a message to %s. \"%s\" (%s)" % (self.name, other.name, reply, identifier))
			other.receive_message(self, reply, identifier)


if __name__ == '__main__':
	A = Agent("A")
	B = Agent("B")
	C = Agent("C")
	D = Agent("D")

	A.agents = [B, C, D]
	B.agents = [A, C, D]

messages_A = ['hello', 'spam', 'message', 'bye']
messages_B = ['hi', 'spam2', 'empty', 'goodbye']


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