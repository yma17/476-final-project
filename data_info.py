import os
import glob

files_to_read = glob.glob("data/all-2015-02-0[1234567]*.txt")
total_files = len(files_to_read)
i = 0
num_data_pts = 0

streamer_set = set()
game_set = set()
game_dict = {}

for filename in glob.glob("data/all-2015-02-0[1234567]*.txt"):
    with open(filename, 'r', encoding='utf-8', errors='replace') as data_file:
        data_file_contents = data_file.readlines()

        for data_pt in data_file_contents:
            num_data_pts += 1
            pt_data = data_pt.strip('\n').split('\t')
            if len(pt_data) == 16:  # all fields present in data point
                streamer = pt_data[4]
                streamer_set.add(streamer)
                game = pt_data[3].lower()
                if game not in game_set:
                    game_set.add(game)
                    game_dict[game] = 0
                game_dict[game] += 1

        i += 1
        print(str(num_data_pts) + " data points so far")
        print(str(len(streamer_set)) + " streamers so far")
        print(str(len(game_set)) + " games so far")
        print("Files read: " + str(i) + "/" + str(total_files))

# t_stop = perf_counter()

# print(t_stop - t_start)

print("Number of streamers: " + str(len(streamer_set)))
#print("List of streamers:")
#for streamer in streamer_set:
#    print(streamer)
print("Number of games: " + str(len(game_set)))
#print("List of games:")
#for game in game_set:
#    print(game)
#for game, count in game_dict.items():
#    if count >= 100:
#        print(str(game) + " " + str(count))
