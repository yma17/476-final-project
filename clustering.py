import numpy as np
from collections import OrderedDict
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from pyclustering.cluster.cure import cure
from pyclustering.utils import read_sample
import matplotlib.pyplot as plt
import pickle

from CommunityAnalysis import get_most_played_game


def dim_reduction(X):
    """Perform dimensionality reduction on the input matrix using PCA."""

    pca = PCA(n_components=30)
    pca.fit(X)
    X = pca.transform(X)

    with open("results/pca_result.txt", "w") as fp:
        np.savetxt(fp, X)

    return X


def k_means_clustering(X, k=-1):
    """Perform k means algorithm."""

    if k == -1:
        begin = 5
        end = 1001
    else:
        begin = k
        end = k + 1

    for k in range(begin, end, 5):
        print(str(k) + " clusters started for k-means")
        kmeans = KMeans(n_clusters=k).fit(X)
        labels = kmeans.labels_

        clusters = []
        for i in range(k):
            row = []
            for j in range(len(labels)):
                if i == labels[j]:
                    row.append(j)
            clusters.append(row)

        results_file = open('results/k_means_' + str(k) + '.pickle', 'wb')
        pickle.dump(clusters, results_file)
        results_file.close()

        print(str(k) + " clusters completed. Score: " + str(kmeans.score(X)))


def cure_clustering(k=-1):
    """Perform CURE clustering algorithm."""

    if k == -1:
        begin = 5
        end = 1001
    else:
        begin = k
        end = k + 1

    input_data = read_sample("results/pca_result.txt")

    for k in range(begin, end, 5):
        print(str(k) + " clusters started for CURE")
        cure_instance = cure(input_data, k)
        cure_instance.process()
        cure_clusters = cure_instance.get_clusters()
        print(str(k) + " clusters completed for CURE")

        results_file = open('results/cure_' + str(k) + '.pickle', 'wb')
        pickle.dump(cure_clusters, results_file)
        results_file.close()


def visualize(k, pca_result, cure_result, kmeans_result, streamer_id_list):
    """Visualize results of clustering."""

    # Visualize results of CURE algorithm first.
    print("Visualizing results for CURE algorithm for k=" + str(k) + " (wait for plot to generate)")

    size_dict = {}
    for i in range(len(cure_result)):
        size_dict[len(cure_result[i])] = i
    size_dict = OrderedDict(sorted(size_dict.items(), reverse=True))

    i = 0
    colors = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']
    for key, value in size_dict.items():
        if i == len(colors):
            break

        cluster_pts = []
        for streamer in cure_result[value]:
            cluster_pts.append(pca_result[streamer])
        cluster_pts = np.array(cluster_pts)

        if len(cluster_pts) == 1:  # at least 2 points in cluster required for t-SNE
            i += 1
            continue

        cure_embedded = TSNE(n_components=2).fit_transform(cluster_pts)
        label = "cluster " + str(value) + ": " + str(key)
        plt.scatter(cure_embedded[:,0], cure_embedded[:,1],
                    s=50, c=colors[i], marker='s', edgecolor='black',
                    label=label)
        i += 1

    plt.title("t-SNE visualization of CURE algorithm results (k=" + str(k) + ")")
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.show()
    plt.clf()

    # Then, visualize results of k-means algorithm.
    print("Visualizing results for k-means algorithm for k=" + str(k) + " (wait for plot to generate)")

    size_dict = {}
    for i in range(len(kmeans_result)):
        size_dict[len(kmeans_result[i])] = i
    size_dict = OrderedDict(sorted(size_dict.items(), reverse=True))

    i = 0
    colors = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w', 'orange', 'lightgreen']
    for key, value in size_dict.items():
        if i == len(colors):
            break
        elif key == 1:
            break

        cluster_pts = []
        for streamer in kmeans_result[value]:
            cluster_pts.append(pca_result[streamer])
        cluster_pts = np.array(cluster_pts)

        if len(cluster_pts) == 1:  # at least 2 points in cluster required for t-SNE
            i += 1
            continue

        cure_embedded = TSNE(n_components=2).fit_transform(cluster_pts)
        label = "cluster " + str(value) + ": " + str(key)
        plt.scatter(cure_embedded[:, 0], cure_embedded[:, 1],
                    s=50, c=colors[i], marker='s', edgecolor='black',
                    label=label)
        i += 1

    plt.title("t-SNE visualization of k-means algorithm results (k=" + str(k) + ")")
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.show()


def games_per_cluster(k, cure_result, kmeans_result, streamer_id_list):
    """Identify the most popular games played per cluster."""

    # First, CURE.
    print("Writing games per cluster for CURE algorithm (results/cure_cluster_games_" + str(k) + ".txt")

    cure_dict = {}
    cure_number_dict = {}
    for i in range(len(cure_result)):
        cure_dict[i] = []
        for streamer_index in cure_result[i]:
            cure_dict[i].append(str(streamer_id_list[streamer_index]))
        cure_number_dict[i] = len(cure_dict[i])

    order_list = sorted(cure_number_dict.items(), key=lambda x: x[1])
    order_list.reverse()

    cure_out = open("results/cure_cluster_games_" + str(k) + ".txt", "w")
    for cluster in order_list:
        id = cluster[0]
        size = cluster[1]

        cure_out.write("For cluster " + str(id) + " of size " + str(size) + ":\n")
        cure_out.write("Most played games are %s\n" % (get_most_played_game(cure_dict[id], 3)))
        cure_out.write("Members:")
        for member in cure_dict[id]:
            cure_out.write(" " + str(member))
        cure_out.write("\n")
    cure_out.close()

    # Then, k-means.
    print("Writing games per cluster for kmeans algorithm (results/cure_cluster_games_" + str(k) + ".txt")

    kmeans_dict = {}
    kmeans_number_dict = {}
    for i in range(len(kmeans_result)):
        kmeans_dict[i] = []
        for streamer_index in kmeans_result[i]:
            kmeans_dict[i].append(str(streamer_id_list[streamer_index]))
        kmeans_number_dict[i] = len(kmeans_dict[i])

    order_list = sorted(kmeans_number_dict.items(), key=lambda x: x[1])
    order_list.reverse()

    kmeans_out = open("results/kmeans_cluster_games_" + str(k) + ".txt", "w")
    for cluster in order_list:
        id = cluster[0]
        size = cluster[1]

        kmeans_out.write("For cluster " + str(id) + " of size " + str(size) + ":\n")
        kmeans_out.write("Most played games are %s\n" % (get_most_played_game(kmeans_dict[id], 3)))
        kmeans_out.write("Members:")
        for member in cure_dict[id]:
            kmeans_out.write(" " + str(member))
        kmeans_out.write("\n")
    kmeans_out.close()
