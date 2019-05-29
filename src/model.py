import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Defaults
EDGELIST = [('A', 'D'), ('D','A'), ('B', 'A'), ('C','E'), ('A','C'), ('F','F')]
EDGE_LABELS = ['a,b,c', 'b,c']

class Kripke_model():
	def __init__(self):
		self.NODE_SIZE = 200
		self.ARROW_SIZE = 50
		self.EDGE_WIDTH = 2

	def construct_model(self, connected_agents=EDGELIST, agent_knowledge_list=EDGE_LABELS):
		# Build your graph
		G = nx.MultiDiGraph()
		G.add_edges_from(EDGELIST)
		# Plot it
		#nx.draw_networkx(G, with_labels=True, edge_color='r', arrows=True, arrowstyle='->', arrowsize=1.0)
		pos = nx.layout.circular_layout(G)
		nx.draw_networkx_labels(G, pos, color='white')
		nx.draw_networkx_nodes(G, pos, with_labels=True, node_size=self.NODE_SIZE, node_color='green')
		'''
		edges = nx.draw_networkx_edges(G, pos, node_size=NODE_SIZE, arrows=True, arrowstyle='->', 
			edge_color='red', width=EDGE_WIDTH)
		'''
		nx.draw_networkx_edges(G, pos, edgelist=EDGELIST, edge_color='r', arrowstyle='<->')
		labels = dict()
		for idx, edge in enumerate(EDGELIST):
			try:
				labels[edge] = EDGE_LABELS[idx]
			except:
				labels[edge] = ''
		print(labels)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

	def put_data_in_model(self, connected_agents=EDGELIST, agent_knowledge_list=EDGE_LABELS):
		model.construct_model(connected_agents, agent_knowledge_list)

	def show_model(self):
		plt.show()

if __name__ == '__main__':
	model = Kripke_model()
	model.put_data_in_model()
	model.show_model()