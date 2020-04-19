import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import community as community_louvain

def main():
	# Read in Graph: G
	G = nx.Graph()
	# G.add_edges_from([(1, 2,{"weight": 1}), (1, 3,{"weight": 1}), (2, 3,{"weight": 1}), (3, 7,{"weight": 10}), (7, 8,{"weight": 1}), (1, 2,{"weight": 1}) ,
	# 				 (8, 9,{"weight": 1}), (9, 10,{"weight": 1}), (10, 11,{"weight": 1}), (11, 9,{"weight": 1}) ])
	f_in = open("useful_data/louvain_in.txt", "r")
	lines = f_in.readlines()
	for line in lines:
		node1 = line.split(" ")[0]
		node2 = line.split(" ")[1]
		weight = int(line.split(" ")[2].strip("\n") )
		G.add_edges_from([ (node1, node2, {"weight": weight}) ])
	f_in.close()

	# Compute the best partition
	partition = community_louvain.best_partition(G)
	num_set = int(len(set(partition.values())))

	community_dict = {}
	community_number_dict = {}
	for i in range(num_set):
		community_dict[i] = []
	for node, community in partition.items():
		community_dict[community].append(node)
	
	for community in community_dict.keys():
		community_number_dict[community] = len(community_dict[community])

	order_list = sorted(community_number_dict.items(), key=lambda x: x[1])
	order_list.reverse()
	
	# Print Partition result txt
	f_out = open("louvain_result", "w")
	f_out.write("num_community: %s\n"%(str(num_set)))
	for community in order_list:
		id = community[0]
		size = community[1]
		f_out.write("%s: size=%s\n"%(str(id), str(size) ) )
		f_out.write("members:")
		for member in community_dict[id]:
			f_out.write(" " + str(member) )
		f_out.write("\n")
	f_out.close()

	# # Drawing fully #######################################################################################################################
	# color_list = list(mpcolors.cnames.values())
	# pos = nx.spring_layout(G)
	# count = 0
	# # Draw nodes
	# for com in set(partition.values()) :
	# 	count += 1
	# 	list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
	# 	nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = color_list[count], with_labels=True, font_weight='bold')
	# # Draw labels
	# nx.draw_networkx_labels(G, pos)
	# # Draw  edges
	# nx.draw_networkx_edges(G, pos, alpha=0.5)
	# plt.show()
	# # plt.savefig("out.png")
	########################################################################################################################################
	
	# Draw induced graph(node as community) #################################################################################################
	Ginduced = community_louvain.induced_graph(partition, G, weight='weight')
	# # Remove small commnity nodes (top15) -> (top10) -> (top5)
	# top = 5
	# for idx in range(len(order_list))[top:]:
	# 	node_id = order_list[idx][0]
	# 	Ginduced.remove_node(node_id)
	
	pos = nx.spring_layout(Ginduced)
	color_list = list(mpcolors.cnames.values())
	# Draw nodes
	count = 0
	for node in Ginduced.nodes :
		nx.draw_networkx_nodes(Ginduced, pos, nodelist=[node], node_size = (20 + 2 * community_number_dict[node]), node_color = color_list[count], with_labels=True, font_weight='bold')
		count += 1
	# Draw labels
	nx.draw_networkx_labels(Ginduced, pos, alpha=0.5)
	# Draw  edges
	nx.draw_networkx_edges(Ginduced, pos, alpha=0.5)
	plt.show()
	# plt.savefig("out.png")
	##########################################################################################################################################

if __name__ == "__main__":
	main()