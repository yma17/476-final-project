import numpy as np
from collections import OrderedDict
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from pyclustering.cluster.cure import cure
from pyclustering.utils import read_sample
from pyclustering.cluster import cluster_visualizer_multidim
import matplotlib.pyplot as plt
import pickle


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
        kmeans = KMeans(n_clusters=k).fit(X)
        labels = kmeans.labels_

        results_file = open('results/k_means_' + str(k) + '.pickle', 'wb')
        pickle.dump(labels, results_file)
        results_file.close()

        print(str(k) + " clusters completed")


def cure_clustering(k):
    """Perform CURE clustering algorithm."""

    input_data = read_sample("results/pca_result.txt")

    print(str(k) + " clusters started for CURE")
    cure_instance = cure(input_data, k)
    cure_instance.process()
    cure_clusters = cure_instance.get_clusters()
    print(str(k) + " clusters completed for CURE")

    results_file = open('results/cure_' + str(k) + '.pickle', 'wb')
    pickle.dump(cure_clusters, results_file)
    results_file.close()

    # visualizer = cluster_visualizer_multidim()
    # visualizer.append_clusters(cure_clusters, input_data)
    # visualizer.show()


def analyze(X, cure_result, kmeans_result):
    """Analyze results of clustering."""

    size_dict = {}
    for i in range(len(cure_result)):
        size_dict[len(cure_result[i])] = i
    size_dict = OrderedDict(sorted(size_dict.items()))

    i = 0
    for key, value in size_dict.items():
        if i == 1:
            break

        print(key)
        print(value)

        cluster_pts = []
        for streamer in cure_result[value]:
            cluster_pts.append(X[streamer])
        cluster_pts = np.array(cluster_pts)
        cure_embedded = TSNE(n_components=2).fit_transform(cluster_pts)
        plt.scatter(cure_embedded[:,0], cure_embedded[:,1],
                    s=50, c='lightgreen', marker='s', edgecolor='black',
                    label='cluster 1')
        i += 1

    plt.show()
