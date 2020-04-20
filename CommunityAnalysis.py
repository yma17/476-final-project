import sys
import pickle
import numpy as np
from itertools import combinations
def get_most_played_game(streamer_list, top):
	# streamer_list: a list of streamer, ex: ["47161834","44535581","81786118"]
	# top: # of most played game returned (descending from top)
	cleaned_dict_file = open('useful_data/cleaned_dict.pickle', 'rb')
	cleaned_dict = pickle.load(cleaned_dict_file)
	cleaned_dict_file.close()
	data = {}
	for game in cleaned_dict.keys():
		players = list(cleaned_dict[game][0])
		if len(list(set(players) & set(streamer_list) ) ) != 0:
			data[game] = len(list(set(players) & set(streamer_list) ) )
	data_inorder = sorted(data.items(), key=lambda x: x[1])
	data_inorder.reverse()
	return data_inorder[:min(top, len(data_inorder))]

def composition_analysis():
	with open("useful_data/streamer_id_list.pickle", "rb") as streamer_id_list_file:
		streamer_id_list = list(pickle.load(streamer_id_list_file) )
	with open("results/cure_" + str(130) + ".pickle", "rb") as cure_file:
		cure_result = list(pickle.load(cure_file) )
	with open("results/k_means_" + str(130) + ".pickle", "rb") as kmeans_file:
		kmeans_result = list(pickle.load(kmeans_file) )
	with open("community_result.pickle", "rb") as community_file:
		community_dict = pickle.load(community_file)
	
	# Filled cure_clusters with streamer ID
	cure_clusters = []
	for cluster in cure_result:
		member_list = []
		for streamerIdx in cluster:
			streamerID = str(streamer_id_list[streamerIdx])
			member_list.append(streamerID)
		cure_clusters.append(member_list)
	
	# Filled kmeans_clusters with streamer ID
	kmeans_clusters = []
	for cluster in kmeans_result:
		member_list = []
		for streamerIdx in cluster:
			streamerID = str(streamer_id_list[streamerIdx])
			member_list.append(streamerID)
		kmeans_clusters.append(member_list)
	
	# Get the size-decending order of communities
	community_number_dict = {}
	for community in community_dict.keys():
		community_number_dict[community] = len(community_dict[community])

	order_list = sorted(community_number_dict.items(), key=lambda x: x[1])
	order_list.reverse()

	# Generate community composition 
	# cure_clusters
	f_out = open("community_cure_composition", "w")
	for order in order_list:
		community_id = order[0]
		community_size = order[1]
		member_list_com = community_dict[community_id]
		composition = {}
		for i in range(len(cure_clusters)):
			member_list_cluster = cure_clusters[i]
			if len( list( set(member_list_com) & set(member_list_cluster) ) ) > 0:
				composition[i] = len( list( set(member_list_com) & set(member_list_cluster) ) ) 
		
		for cluster_id in composition.keys():
			composition[cluster_id] = round(float(composition[cluster_id])/float(community_size) * 100.0, 2)
		
		composition_list = sorted(composition.items(), key=lambda x: x[1])
		composition_list.reverse()

		f_out.write("Community %s: size=%s\n" % (str(community_id), str(community_size) ) )
		f_out.write("Composition: %s\n" % (composition_list) )
	f_out.close()
	# kmeans_clusters
	f_out = open("community_kmeans_composition", "w")
	for order in order_list:
		community_id = order[0]
		community_size = order[1]
		member_list_com = community_dict[community_id]
		composition = {}
		for i in range(len(kmeans_clusters)):
			member_list_cluster = kmeans_clusters[i]
			if len( list( set(member_list_com) & set(member_list_cluster) ) ) > 0:
				composition[i] = len( list( set(member_list_com) & set(member_list_cluster) ) ) 
		
		for cluster_id in composition.keys():
			composition[cluster_id] = round(float(composition[cluster_id])/float(community_size) * 100.0, 2)
		
		composition_list = sorted(composition.items(), key=lambda x: x[1])
		composition_list.reverse()

		f_out.write("Community %s: size=%s\n" % (str(community_id), str(community_size) ) )
		f_out.write("Composition: %s\n" % (composition_list) )
	f_out.close()

if __name__ == "__main__":
	print(get_most_played_game(["47161834","44535581","81786118","40979006", "47962448", "40106353", "63284189", "44094998", "41000942", "53979464", "71588258", "54441635", "61805742"], 3) )
	composition_analysis()