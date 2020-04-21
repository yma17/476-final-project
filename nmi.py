"""Script to compute NMI between community and clustering results"""

import sys
import pickle

from sklearn.metrics import normalized_mutual_info_score


def get_nmi(argv):
    # Get result from community source.
    with open(argv[0], 'rb') as src_1:
        louvain_result = pickle.load(src_1)

        if type(louvain_result) == dict:
            with open('useful_data/streamer_indices.pickle', 'rb') as streamer_ind_file:
                streamer_ind = pickle.load(streamer_ind_file)

                # Modify format of community source for commonality with clustering result.
                louvain_modified = [[] for i in range(len(louvain_result))]
                for key, value in louvain_result.items():
                    louvain_modified[key] = [streamer_ind[int(s)] for s in value]
                louvain_result = louvain_modified

        # Preprocess in preparation for NMI.
        louvain_nmi = [0 for i in range(7543)]  # value hardcoded
        for i in range(len(louvain_result)):
            for j in louvain_result[i]:
                louvain_nmi[j] = i

    # Get result from clustering source.
    with open(argv[1], 'rb') as src_2:
        clustering_result = pickle.load(src_2)

        # Preprocess in preparation for NMI.
        clustering_nmi = [0 for i in range(7543)]  # value hardcoded
        for i in range(len(clustering_result)):
            for j in clustering_result[i]:
                clustering_nmi[j] = i

    # Calculate NMI.
    print("NMI: ")
    print(normalized_mutual_info_score(clustering_nmi, louvain_nmi))


if __name__ == '__main__':
    get_nmi(sys.argv[1:])