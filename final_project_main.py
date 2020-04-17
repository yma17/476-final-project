"""Main function for final project."""

import sys
import getopt

from read_data import read_raw_files, read_useful_files, clean_game_names
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
    if method == "" or source == "":
        print("Not all parameters are specified")
        sys.exit(1)

    # Read the data (from the command-line specified source)
    if source == "raw":
        streamer_set, game_dict, game_corpus = read_raw_files()
    elif source == "useful":
        streamer_set, game_dict, game_corpus = read_useful_files()

    # Simple test case
    # from collections import Counter
    # streamer_set = {1, 2, 3}
    # game_dict = {"aaaa": [{1, 2}, Counter([1, 2])],
    #              "axxa": [{1, 3}, Counter([1, 1, 3])],
    #              "bbbb": [{2, 3}, Counter([2, 2, 3, 3])],
    #              "cccc": [{1, 2, 3}, Counter([1, 1, 2, 2, 3, 3])]
    # game_corpus = {"aaaa", "bbbb"}

    # Preprocess the data.
    cleaned_dict = clean_game_names(game_dict, game_corpus)

    # Perform community detection on the data.
    pass

    # Perform clustering on the data.
    pass


if __name__ == '__main__':
    main(sys.argv[1:])