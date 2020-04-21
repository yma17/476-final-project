"""Main function for final project."""

import sys
import getopt
import pickle
import numpy as np

from preprocessing import read_raw_files, \
    clean_game_names, construct_feature_space
from CommunityDetection import community_detection
from clustering import dim_reduction, k_means_clustering, cure_clustering, \
    visualize, games_per_cluster


def main(argv):
    # Parse command line arguments.
    command = ""
    k = -1
    try:
        opts, args = getopt.getopt(argv, "k:", ["command="])
    except:
        print("Incorrectly specified parameter")
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--command":
            command = arg
        elif opt == "-k":
            k = int(arg)
    if command == "":
        print("Not all required parameters are specified")
        sys.exit(1)

    # Read the data (from the command-line specified source) + preprocess it.
    if command == "preprocess":
        game_dict, game_corpus = read_raw_files()
        clean_game_names(game_dict, game_corpus)
        return

    # Read in preprocessed data.
    streamer_set = set()
    streamer_file = open('useful_data/streamer.txt', 'r')
    streamer_data = streamer_file.readlines()
    for i in streamer_data:
        streamer_set.add(int(i[:-1]))
    streamer_file.close()
    cleaned_dict_file = open('useful_data/cleaned_dict.pickle', 'rb')
    cleaned_dict = pickle.load(cleaned_dict_file)
    cleaned_dict_file.close()

    if command == "community":
        X = construct_feature_space(streamer_set, cleaned_dict, command)
        community_detection()  # analysis of community detection within this function.
        return
    elif command == "clustering_kmeans":
        if k == -1:
            print("k not specified. Will run on all k from 5 to 1000 in intervals of 5.")

        X = construct_feature_space(streamer_set, cleaned_dict, command)
        X = dim_reduction(X)
        k_means_clustering(X, k)
    elif command == "clustering_cure":
        if k == -1:
            print("k not specified. Will run on all k from 5 to 1000 in intervals of 5.")

        X = construct_feature_space(streamer_set, cleaned_dict, command)
        dim_reduction(X)
        cure_clustering(k)
    elif command == "analyze_clusters":
        with open("useful_data/streamer_id_list.pickle", "rb") as streamer_id_list_file:
            streamer_id_list = pickle.load(streamer_id_list_file)
        with open("results/pca_result.txt", "r") as pca_result_file:
            pca_result = np.loadtxt(pca_result_file, delimiter=' ', dtype=np.int8)
        with open("results/cure_" + str(k) + ".pickle", "rb") as cure_file:
            cure_result = pickle.load(cure_file)
        with open("results/k_means_" + str(k) + ".pickle", "rb") as kmeans_file:
            kmeans_result = pickle.load(kmeans_file)

        visualize(k, pca_result, cure_result, kmeans_result, streamer_id_list)
        games_per_cluster(k, cure_result, kmeans_result, streamer_id_list)


if __name__ == '__main__':
    main(sys.argv[1:])