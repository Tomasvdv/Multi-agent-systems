import random
import numpy as np

class Agent:
	def __init__(self, name):
		self.FAIL_PROB = 0.0
		self.knowledge = set([]) #sets can't contain duplicates.
		self.sent_messages = [] 
		self.received_messages = []

		self.agents = []
		self.name = str(name)
		self.messageidx = 0
		self.confirmed = np.zeros(100) #initial size

	def send_new_message(self, other, message):
		print("%s sent a message to %s. \"%s\" (%d)" % (self.name, other.name, message, self.messageidx))
		self.sent_messages.append((message, self.messageidx, other))
		other.receive_message(self, message, self.messageidx)
		self.messageidx += 1

	# def resend_message(self, other, message, messageidx):
	# 	print("%s resent a message to %s. \"%s\" (%d)" % (self.name, other.name, message, messageidx))
	# 	other.receive_message(self, message, messageidx)

	def resend_last_message(self, idx):
		for lidx in range(len(self.sent_messages)-1, -1, -1): #loop from last message to first
			(message, midx, other) = self.sent_messages[lidx]
			if midx == idx:
				print("%s resent a message to %s. \"%s\" (%d)" % (self.name, other.name, message, midx))
				other.receive_message(self, message, midx)
				return
		print("could not find message", idx)
		print(self.sent_messages)

	def receive_message(self, other, message, idx):
		successfully_received = random.random() > self.FAIL_PROB
		if successfully_received:
			self.knowledge.add(message)
			self.received_messages.append((message, idx, other))
			print("%s successfully received a message! \"%s\"" % (self.name, message))
			self.send_reply(other, message, idx)

			

	def send_reply(self, other, message, idx):
		if message.startswith("K_"):
			reply = "K_%s(%s)"  % (self.name, message)
		else:
			reply = "K_%s(%d)"  % (self.name, idx)

		self.knowledge.add(reply) #add the reply to knowledge base

		if reply.count("K_%s" % self.name) == 2 and reply.count("K") == 4: #e.g. K_a(K_b(K_a(K_b(1))))
			self.confirmed[idx] = 1
		else:
			self.sent_messages.append((reply, idx, other))
			print("%s resent a message to %s. \"%s\" (%d)" % (self.name, other.name, reply, idx))
			other.receive_message(self, reply, idx)


if __name__ == '__main__':
	A = Agent("A")
	B = Agent("B")

	A.agents.append(B)
	B.agents.append(A)

messages = ['hello', 'spam', 'message', 'bye']

for message in messages:
	A.send_new_message(B, message)

running = True
while running:
	running = False
	# print("confirmed: ", np.sum(A.confirmed), A.confirmed)
	for idx in range(len(messages)):
		if A.confirmed[idx] != 1: #not yet confirmed
			# print("message ", idx, "resending")
			A.resend_last_message(idx)
			running = True



