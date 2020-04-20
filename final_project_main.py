"""Main function for final project."""

import sys
import getopt
import pickle
import glob
import numpy as np

from preprocessing import read_raw_files, read_useful_files, \
    clean_game_names, construct_feature_space
# from community_detection
from clustering import dim_reduction, k_means_clustering, cure_clustering, \
    visualize, games_per_cluster


def main(argv):
    # Parse command line arguments.
    method = ""
    source = ""
    k = -1
    try:
        opts, args = getopt.getopt(argv, "k:", ["method=", "source="])
    except:
        print("Incorrectly specified parameter")
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--method":
            method = arg
        elif opt == "--source":
            source = arg
        elif opt == "-k":
            k = int(arg)
    if (method != "community" and method != "clustering_cure"
        and method != "clustering_kmeans" and method != "none") or \
        (source != "raw" and source != "extracted" and
         source != "cleaned" and source != "result"):
        print("Not all required parameters are specified")
        sys.exit(1)

    # Read the data (from the command-line specified source) + preprocess it.
    if source == "raw":
        streamer_set, game_dict, game_corpus = read_raw_files()
        cleaned_dict = clean_game_names(game_dict, game_corpus)
    elif source == "extracted":
        streamer_set, game_dict, game_corpus = read_useful_files()
        cleaned_dict = clean_game_names(game_dict, game_corpus)
    elif source == "cleaned":
        streamer_set = set()
        streamer_file = open('useful_data/streamer.txt', 'r')
        streamer_data = streamer_file.readlines()
        for i in streamer_data:
            streamer_set.add(int(i[:-1]))
        streamer_file.close()
        cleaned_dict_file = open('useful_data/cleaned_dict.pickle', 'rb')
        cleaned_dict = pickle.load(cleaned_dict_file)
        cleaned_dict_file.close()
    elif source == "result":
        if k == -1:
            print("k not specified")
            sys.exit(1)

        with open("useful_data/streamer_id_list.pickle", "rb") as streamer_id_list_file:
            streamer_id_list = pickle.load(streamer_id_list_file)
        with open("results/pca_result.txt", "r") as pca_result_file:
            pca_result = np.loadtxt(pca_result_file, delimiter=' ', dtype=np.int8)
        with open("results/cure_" + str(k) + ".pickle", "rb") as cure_file:
            cure_result = pickle.load(cure_file)
        with open("results/k_means_" + str(k) + ".pickle", "rb") as kmeans_file:
            kmeans_result = pickle.load(kmeans_file)


        # visualize(pca_result, cure_result, kmeans_result, streamer_id_list)
        games_per_cluster(cure_result, kmeans_result, streamer_id_list)
        return

    if method == "none":
        pass
    elif method == "community":
        X = construct_feature_space(streamer_set, cleaned_dict, method)
        pass
    elif method == "clustering_kmeans":
        X = construct_feature_space(streamer_set, cleaned_dict, method)
        X = dim_reduction(X)
        k_means_clustering(X, k)
    elif method == "clustering_cure":
        if k == -1:
            print("k not specified")
            sys.exit(1)
        X = construct_feature_space(streamer_set, cleaned_dict, method)
        dim_reduction(X)
        cure_clustering(k)


if __name__ == '__main__':
    main(sys.argv[1:])