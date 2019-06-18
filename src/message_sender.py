import random


class Message_sender:
	def __init__(self, model):
		self.model = model #save messageprotocol and failprob in model for easy swapping in GUI

	def send_message(self, agent1, agent2, message):
		if self.model.messageprotocol == 'A1':
			self.send_message_A1(agent1, agent2, message)
		else: ## use TCP
			self.send_message_TCP(agent1, agent2, message)

	def resend_message(self, agent1, identifier):
		if self.model.messageprotocol == 'A1':
			self.resend_message_A1(agent1, identifier)
		else: ## use TCP
			self.resend_message_TCP(agent1, identifier)

	def reply(self, agent1, agent2, message, identifier = 0):
		if self.model.messageprotocol == 'A1':
			self.reply_A1(agent1, agent2, message, identifier)
		else: ## use TCP
			self.reply_TCP(agent1, agent2, message)

	def check_inbox(self, agent1):
		if self.model.messageprotocol == 'A1':
			self.check_inbox_A1(agent1)
		else: ## use TCP
			self.check_inbox_TCP(agent1)

	def send_message_TCP(self, agent1, agent2, message):
		if random.random() > self.model.failprob:
			agent2.inbox.append((agent1, message))
		agent1.sent_messages.append((message, 0, agent2)) ## 0 is to give it the same length as A1 protocol
		agent1.confirmed[agent1.messageidx] = 0 ## ack is not yet received (remodel confirmed for use for ack)
		agent1.messageidx += 1

	def resend_message_TCP(self, agent1, messageidx):
		message, _,  agent2 = agent1.sent_messages[messageidx]
		if random.random() > self.model.failprob:
			agent2.inbox.append((agent1, message))

	def reply_TCP(self, agent1, agent2, message):
		message = "ack(%s)" % message
		if random.random() > self.model.failprob:
			agent2.inbox.append((agent1, message))

	def send_message_A1(self, agent1, agent2, message):
		identifier = str(agent1.messageidx) + agent1.name
		agent1.sent_messages.append((message, identifier, agent2))
		if random.random() > self.model.failprob:
			agent2.inbox.append((agent1, identifier, message))
		agent1.update_message_manager(agent2, message, identifier, 'send')
		agent1.confirmed[identifier] = 0
		agent1.messageidx += 1


	def resend_message_A1(self, agent1, identifier):
		for idx in range(len(agent1.sent_messages)-1, -1, -1): #loop from last message to first
			(message, midentifier, other) = agent1.sent_messages[idx]
			if midentifier == identifier:
				agent1.update_message_manager(other, message, identifier, 'resend')
				if random.random() > self.model.failprob:
					other.inbox.append((agent1, identifier, message))
				return


	def reply_A1(self, agent1, agent2, message, identifier):
		reply = "K_%s(%s)"  % (agent1.name, message)

		agent1.knowledge.add(reply) #add the reply to knowledge base

		if reply.count("K_%s" % agent1.name) >= 2 and reply.count("K_") == 4: #e.g. K_a(K_b(K_a(K_b(1))))
			agent1.confirmed[identifier] = 1
		else:
			agent1.sent_messages.append((reply, identifier, agent2))
			agent1.update_message_manager(agent2, reply, identifier, 'reply')

			if random.random() > self.model.failprob:
				agent2.inbox.append((agent1, identifier, reply))

	def check_inbox_A1(self, agent1):
		for (other, identifier, message) in agent1.inbox:
			agent1.knowledge.add(message)
			agent1.received_messages.append((message, identifier, other))
			agent1.update_message_manager(other, message, identifier, 'receive')
			agent1.send_reply(other, message, identifier)

	def check_inbox_TCP(self, agent1):
		for (other, message) in agent1.inbox:
			agent1.knowledge.add(message)
			agent1.received_messages.append((message, 0, other))
			agent1.update_message_manager(other, message, 0, 'receive')

			if message.startswith('ack'):
				## find index of message
				original_message = (message.split("(")[1]).split(")")[0]
				idx = agent1.sent_messages.index((original_message, 0, other))
				agent1.confirmed[idx] = 1
			else:
				agent1.send_reply(other, message, 0)