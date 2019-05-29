import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Defaults
EDGELIST = [('P', '!P'), ('!P', 'P'), ('P', 'P')]
EDGE_LABELS = ['a,b,c',]
NODE_LABELS = ['refl: ', 'refl: ']

class Kripke_model():
	def __init__(self):
		self.NODE_SIZE = 200
		self.NODE_SIZE_REFL = 20
		self.ARROW_SIZE = 50
		self.EDGE_WIDTH = 2
		self.REFL_FONTSIZE = 8

	# get knowledge from knowledge dictionary
	def get_knowledge(self, knowledge_dict):
		for key, val in knowledge_dict.items():
			#Read stuff

			pass

	def construct_model(self, connected_agents=EDGELIST, agent_knowledge_list=EDGE_LABELS):
		# Build your graph
		G = nx.MultiDiGraph()
		G.add_edges_from(EDGELIST)
		# Plot it
		#pos = nx.layout.circular_layout(G)
		pos = nx.layout.spring_layout(G)
		print(pos)

		nx.draw_networkx_labels(G, pos, color='white')
		labels = dict()
		for idx, (key, value) in enumerate(pos.items()):
			labels.update({key:'\n\n\n'+str(NODE_LABELS[idx])})
		print(labels)
		nx.draw_networkx_labels(G, pos, labels=labels, color='white', font_size=self.REFL_FONTSIZE)
		
		nx.draw_networkx_nodes(G, pos, with_labels=True, node_size=self.NODE_SIZE, node_color='green')
		nx.draw_networkx_edges(G, pos, edgelist=EDGELIST, edge_color='r', arrowstyle='<->')
		labels = dict()
		for idx, edge in enumerate(EDGELIST):
			try:
				labels[edge] = EDGE_LABELS[idx]
			except:
				labels[edge] = ''
		#print(labels)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

	def put_data_in_model(self, connected_agents=EDGELIST, agent_knowledge_list=EDGE_LABELS):
		model.construct_model(connected_agents, agent_knowledge_list)

	def show_model(self):
		plt.show()

if __name__ == '__main__':
	model = Kripke_model()
	model.put_data_in_model()
	model.show_model()