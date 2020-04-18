from collections import Counter
import pickle
from spell_check import SpellCorrector

#corpus = Counter(["a", "b", "c"])
#sc = SpellCorrector(dictionary=corpus)
#print(sc.correction("島風的褲褲"))

#d = {}
#d["島風的褲褲"] = ([], [])
#d["島風的褲褲"][0].append(1)
#d["島風的褲褲"][1].append(2)
#d["島風的褲褲"][1].append(3)
#print(d)

#d = {"game1": ([1, 2], Counter([1, 2, 3, 4])), "game2": ([5, 6], Counter([2, 3, 4]))}
#testfile = open('test.txt', 'wb')
#pickle.dump(d, testfile)

#testfile = open('test.txt', 'rb')
#e = pickle.load(testfile)
#print(e)

# a = open("useful_data/raw_counter.txt", "r", encoding="utf-8", errors="replace")
# b = a.readlines()
# e = []
# for c in b:
#     d = c.split("\t")
#     for i in range(int(d[2])):
#        e.append(d[1])
# a.close()
# f = Counter(e)
# print(len(f))
# print(f.most_common()[-10600:-10500])

"""
import time
from random import seed
from random import random
from sklearn.cluster import MiniBatchKMeans, KMeans
import numpy as np
import sys
from pyclustering.cluster.cure import cure
from pyclustering.utils import read_sample

X = np.zeros((700000, 4000))
seed(1)
for i in range(700000):
    if i % 1000 == 0:
        print(i)
    for j in range(4000):
        k = random()
        if k < 0.0005:
            X[i][j] = 1

for i in range(10, 1000, 30):
    time1 = time.perf_counter()
    cure_instance = cure(read_sample(X.tolist()), i)
    cure_instance.process()
    cure_clusters = cure_instance.get_clusters()
    time2 = time.perf_counter()
    print("For " + str(i) + " clusters: ")
    print(time2 - time1)
    print("")

    #for j in range(20, 200, 30):
    #    time1 = time.perf_counter()
    #    kmeans = MiniBatchKMeans(n_clusters=i, batch_size=j).fit(X)
    #    time2 = time.perf_counter()
    #    print("For " + str(i) + " clusters and " + str(j) + " batch size: ")
    #    print(time2 - time1)
    #    print("")
"""

cleaned_dict_file = open('useful_data/cleaned_dict.pickle', 'rb')
cleaned_dict = pickle.load(cleaned_dict_file)
i = 0
for game, info in cleaned_dict.items():
    if len(info[0]) > 3:
        i += 1

print(i)