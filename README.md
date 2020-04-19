# 476-final-project
Final project for EECS 476 W20.

How to use:
1. Contents of the useful_data directory: already preprocessed data.
2. Contents of the raw_data directory: raw data for project.
3. Ensure the following packages are present: symspellpy, sklearn, pyclustering.
4. Run the python file final_project_main.py the following required parameters: "--method" (specify either "clustering_kmeans", "clustering_cure", or "community", depending on the algorithm desired to run) and "--source" (specify either "raw" to read raw data if files exist, "extracted" to read already extracted most useful columns, or "cleaned" to read already preprocessed data).
