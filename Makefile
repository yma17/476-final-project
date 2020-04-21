default: all

all:
	@echo "Follow README.md instructions."

preprocess:
	@python final_project_main.py --command preprocess

community:
	@python final_project_main.py --command community

clustering_kmeans:
ifdef k
	@python final_project_main.py --command clustering_kmeans -k $(k)
else
	@python final_project_main.py --command clustering_kmeans
endif

clustering_cure:
ifdef k
	@python final_project_main.py --command clustering_cure -k $(k)
else
	@python final_project_main.py --command clustering_cure
endif

analyze_clusters:
ifdef k
	@python final_project_main.py --command analyze_clusters -k $(k)
else
	@echo "Please specify the number of clusters (e.g. k=100)".
endif
