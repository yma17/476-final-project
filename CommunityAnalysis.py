import pickle
from itertools import combinations
def get_most_played_game(streamer_list, top):
	# streamer_list: a list of streamer, ex: ["47161834","44535581","81786118"]
	# top: # of most played game returned (descending from top)
	cleaned_dict_file = open('useful_data/cleaned_dict.pickle', 'rb')
	cleaned_dict = pickle.load(cleaned_dict_file)
	cleaned_dict_file.close()
	data = {}
	for game in cleaned_dict.keys():
		players = list(cleaned_dict[game][0])
		if len(list(set(players) & set(streamer_list) ) ) != 0:
			data[game] = len(list(set(players) & set(streamer_list) ) )
	data_inorder = sorted(data.items(), key=lambda x: x[1])
	data_inorder.reverse()
	return data_inorder[:min(top, len(data_inorder))]

if __name__ == "__main__":
	print(get_most_played_game(["47161834","44535581","81786118","40979006", "47962448", "40106353", "63284189", "44094998", "41000942", "53979464", "71588258", "54441635", "61805742"], 3) )