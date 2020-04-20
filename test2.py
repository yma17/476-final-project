import sys
import pickle
import numpy as np

def main():
	with open("useful_data/streamer_id_list.pickle", "rb") as streamer_id_list_file:
		streamer_id_list = pickle.load(streamer_id_list_file)
	with open("results/cure_" + str(130) + ".pickle", "rb") as cure_file:
		cure_result = pickle.load(cure_file)
	with open("results/k_means_" + str(130) + ".pickle", "rb") as kmeans_file:
		kmeans_result = pickle.load(kmeans_file)
	with open("community_result.pickle", "rb") as community_file:
		community_dict = pickle.load(community_file)
	
	# Filled cure_clusters with streamer ID
	cure_clusters = []
	for cluster in cure_result:
		member_list = []
		for streamerIdx in cluster:
			streamerID = streamer_id_list[streamerIdx]
			member_list.append(streamerID)
		cure_clusters.append(member_list)
	
	# Filled kmeans_clusters with streamer ID
	kmeans_clusters = []
	for cluster in kmeans_result:
		member_list = []
		for streamerIdx in cluster:
			streamerID = streamer_id_list[streamerIdx]
			member_list.append(streamerID)
		cure_clusters.append(member_list)

	# Get the size-decending order of communities
	community_number_dict = {}
	for community in community_dict.keys():
		community_number_dict[community] = len(community_dict[community])

	order_list = sorted(community_number_dict.items(), key=lambda x: x[1])
	order_list.reverse()

	# Generate community composition 
	

if __name__ == "__main__":
	main()