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

X = np.zeros((623257, 6434), dtype=np.int8)
print(sys.getsizeof(X))
seed(1)
for i in range(623257):
    if i % 1000 == 0:
        print(i)
    for j in range(6434):
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
print(len(cleaned_dict))


"""
import glob
stream_data = glob.glob("raw_data/all-2015-02-0[1234567]*.txt")
streamer_set = set()
game_set = set()
total_stream_files = len(stream_data)
i = 0

for filename in stream_data:
    with open(filename, 'r', encoding='utf-8', errors='replace') as stream_file:
        stream_file_contents = stream_file.readlines()

        for data_pt in stream_file_contents:
            pt_data = data_pt.strip('\n').split('\t')
            if len(pt_data) == 16:  # check if all fields are present in data point
                streamer = pt_data[4]
                viewers = int(pt_data[1])
                game = pt_data[3].lower()
                if viewers >= 100:
                    streamer_set.add(streamer)
                    if game != -1:
                        game_set.add(game)

    i += 1
    print(i)

print("")
print(len(streamer_set))
print(len(game_set))
"""

"""
corpus_file = open('useful_data/corpus.txt', 'r')
corpus_data = corpus_file.readlines()
game_corpus = set()
for game in corpus_data:
    game_corpus.add(game)
corpus_file.close()

game_dict_file = open('useful_data/game_dict.pickle', 'rb')
game_dict = pickle.load(game_dict_file)
game_dict_file.close()

#for i in game_dict.keys():
#    if i == 'grand theft auto v':
#        print(len(i))

for j in game_corpus:
    if j == 'grand theft auto v\n':
        print("yes")

# cleaned_names = set(game_dict.keys()).intersection(game_corpus)
# print(len(cleaned_names))
"""