import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import community as community_louvain

def main():
	# Read in Graph: G
	G = nx.Graph()
	G.add_edges_from([(1, 2,{"weight": 1}), (1, 3,{"weight": 1}), (2, 3,{"weight": 1}), (3, 7,{"weight": 10}), (7, 8,{"weight": 1}), (1, 2,{"weight": 1}) ,
					 (8, 9,{"weight": 1}), (9, 10,{"weight": 1}), (10, 11,{"weight": 1}), (11, 9,{"weight": 1}) ])

	# Compute the best partition
	partition = community_louvain.best_partition(G)
	num_set = int(len(set(partition.values())))
	print("num_set:", str(num_set) )
	print("partition:", partition)
	

	# Drawing
	color_list = list(mpcolors.cnames.values())
	pos = nx.spring_layout(G)
	count = 0
	# Draw nodes
	for com in set(partition.values()) :
		count += 1
		list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
		nx.draw_networkx_nodes(G, pos, list_nodes, node_color = color_list[count], with_labels=True, font_weight='bold')
	# Draw labels
	nx.draw_networkx_labels(G, pos)
	# Draw  edges
	nx.draw_networkx_edges(G, pos, alpha=0.5)
	plt.show()
	# plt.savefig("out.png")

if __name__ == "__main__":
	main()