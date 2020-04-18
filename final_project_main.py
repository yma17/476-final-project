"""Main function for final project."""

import sys
import getopt
import pickle


from preprocessing import read_raw_files, read_useful_files, \
    clean_game_names, construct_feature_space
# from community_detection
# from clustering


def main(argv):
    # Parse command line arguments.
    method = ""
    source = ""
    try:
        opts, args = getopt.getopt(argv, "", ["method=", "source="])
    except:
        print("Incorrectly specified parameter")
        sys.exit(1)
    for opt, arg in opts:
        if opt == "--method":
            method = arg
        elif opt == "--source":
            source = arg
    if (method != "community" and method != "clustering") or \
        (source != "raw" and source != "extracted" and
         source != "cleaned"):
        print("Not all parameters are specified")
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

    # Simple test case
    # from collections import Counter
    # streamer_set = {1, 2, 3, 4}
    # cleaned_dict = {"aaaa": [{1, 2}, Counter([1, 2])],
    #              "axxa": [{1, 3}, Counter([1, 1, 3])],
    #              "bbbb": [{2, 3}, Counter([2, 2, 3, 3])],
    #              "cccc": [{1, 2, 3}, Counter([1, 1, 2, 2, 3, 3])],
    #              "z": [{1, 2, 4}, Counter({1, 2, 4, 4, 4, 4})]}

    X = construct_feature_space(streamer_set, cleaned_dict, method)
    # TODO: do louvain or clustering here.


if __name__ == '__main__':
    main(sys.argv[1:])