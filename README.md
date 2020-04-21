# 476-final-project
Final project for EECS 476 W20.

How to use:
1. Under raw_data, only a subset of the original dataset was included, spanning only the first day. To access the full dataset, visit https://clivecast.github.io/
2. Ensure the following packages are present: symspellpy, sklearn, pyclustering, networkx, community, matplotlib.
3. The following commands are used to run the code:
* "make preprocess" to perform initial preprocessing on the data. This stage includes initial feature selection and game title cleaning. The game title cleaning portion takes a while to run, so you may have to wait a while.
* "make community" to perform the community detection algorithm (Louvain's) and produce the results.
* "make clustering_kmeans k=[parameter]" to perform the k-means clustering algorithm. If k (number of clusters) is not specified, the algorithm will run on all k from 5 to 1000 in intervals of 5.
* "make clustering_cure k=[parameter]" to perform the CURE clustering algorithm. If k (number of clusters) is not specified, the algorithm will run on all k from 5 to 1000 in intervals of 5.
* "make analyze_clusters k=[parameter]" to visualize the results of the two clustering algorithms run with k clusters and produce the results. k must be specified, and the results of both clustering algorithms run with k clusters must be present.
4. Contents of the CODE folder:
* root: all Python scripts.
* raw_data: all raw data for this project.
* useful_data: all cleaned / preprocessed data for this project.
* results: all results from the clustering algorithms.
* community_plot, community_result, root: all results from the community detection algorithms.
