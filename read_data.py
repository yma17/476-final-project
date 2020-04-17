"""Contains functions to read and preprocess data"""

import os
import glob
import csv
import pickle
from collections import Counter

from spell_check import SpellCorrector


def read_raw_files():
    """Read all raw files necessary for project."""

    # Read in first seven days of streaming data.
    stream_data = glob.glob("raw_data/all-2015-02-0[1234567]*.txt")
    # stream_data = glob.glob("raw_data/all-2015-02-01-00-0[05]-00.txt")
    total_stream_files = len(stream_data)
    i = 0  # keep track of files read
    num_data_pts = 0  # keep track of data points read

    streamer_set = set()  # set of unique streamers
    game_set = set()  # set of (uncleaned) unique game titles

    # dictionary of game :
    #   [set of unique streamers who have played it,
    #   count of five minute intervals for each user]
    game_dict = {}

    for filename in stream_data:
        with open(filename, 'r', encoding='utf-8', errors='replace') as stream_file:
            stream_file_contents = stream_file.readlines()

            for data_pt in stream_file_contents:
                num_data_pts += 1
                pt_data = data_pt.strip('\n').split('\t')
                if len(pt_data) == 16:  # check if all fields are present in data point
                    streamer = pt_data[4]
                    streamer_set.add(streamer)
                    game = pt_data[3].lower()
                    if game != "-1":
                        if game not in game_set:
                            game_set.add(game)
                            game_dict[game] = [set(), []]  # (set of streamers, list of stream occurrences)
                        game_dict[game][0].add(streamer)
                        game_dict[game][1].append(streamer)

            i += 1
            # print(str(num_data_pts) + " data points so far")
            # print(str(len(streamer_set)) + " streamers so far")
            # print(str(len(game_set)) + " games so far")
            print("Files read: " + str(i) + "/" + str(total_stream_files))  # output updates to user

    for game in game_dict.keys():
        game_dict[game] = [game_dict[game][0], Counter(game_dict[game][1])]

    # Read in corpus of names of games for NLP algorithm.
    game_corpus = set()
    with open("raw_data/ign.csv", 'r', encoding='utf-8', errors='replace') as game_file:
        game_file_contents = csv.reader(game_file, delimiter=',')
        for data_pt in game_file_contents:
            game = data_pt[2].lower()
            game_corpus.add(game)

    """
    streamer_file = open('useful_data/streamer.txt', 'w+')
    for streamer in streamer_set:
        streamer_file.write(streamer+'\n')
    streamer_file.close()
    
    game_file = open('useful_data/uncleaned_game.txt', 'w+')
    for game in game_set:
        game_file.write(game+'\n')
    game_file.close()
    
    corpus_file = open('useful_data/corpus.txt', 'w+')
    for game in game_corpus:
        corpus_file.write(game+'\n')
    corpus_file.close()
    game_dict_file = open('useful_data/game_dict.pickle', 'wb')
    pickle.dump(game_dict, game_dict_file)
    game_dict_file.close()
    """

    return streamer_set, game_dict, game_corpus


def read_useful_files():
    """Read most useful data extracted from raw data."""

    streamer_file = open('useful_data/streamer.txt', 'r')
    streamer_data = streamer_file.readlines()
    streamer_set = set()  # set of unique streamers
    for streamer in streamer_data:
        streamer_set.add(streamer)
    streamer_file.close()

    game_dict_file = open('useful_data/game_dict.pickle', 'rb')
    game_dict = pickle.load(game_dict_file)

    corpus_file = open('useful_data/corpus.txt', 'r')
    corpus_data = corpus_file.readlines()
    game_corpus = set()
    for game in corpus_data:
        game_corpus.add(game)
    corpus_file.close()

    return streamer_set, game_dict, game_corpus


def clean_game_names(game_dict, game_corpus):
    """Perform data cleaning on streamer-specified game names."""

    game_replace_dict = get_replacement_dict()
    game_corpus_counter = Counter(game_corpus)
    spell_corrector = SpellCorrector(dictionary=game_corpus_counter)
    cleaned_dict = {}

    # For optimization, find intersection of dataset game names and corpus.
    cleaned_names = set(game_dict.keys()).intersection(game_corpus)
    for name in cleaned_names:
        cleaned_dict[name] = game_dict[name]

    names_to_clean = set(game_dict.keys()).difference(cleaned_names)
    i = len(cleaned_names)

    # Spell correct remainder of names.
    for name in names_to_clean:
        if i % 100 == 0:  # output updates to user
            print(str(i) + " names cleaned")
        i += 1

        if name in game_replace_dict.keys():
            # Remove abbreviation from name.
            corrected_name = game_replace_dict[name]
        else:
            # Correct spelling of name to corpus within 2 edit distance.
            corrected_name = spell_corrector.correction(name)

        cleaned_names.add(corrected_name)
        if corrected_name not in cleaned_dict.keys():
            cleaned_dict[corrected_name] = [set(), Counter([])]

        cleaned_dict[corrected_name][0].update(game_dict[name][0])
        cleaned_dict[corrected_name][1] += game_dict[name][1]

    # print(len(cleaned_dict))

    for name in cleaned_names:
        if len(cleaned_dict[name][0]) == 1:  # if only one player has played a game
            del cleaned_dict[name]
        elif sum(cleaned_dict[name][1].values()) <= 12:  # if a game was never played for more than 1 hour overall
            del cleaned_dict[name]

    # print(len(cleaned_dict))

    cleaned_file = open('useful_data/cleaned_dict.pickle', 'wb')
    pickle.dump(cleaned_dict, cleaned_file)
    cleaned_file.close()

    return cleaned_dict


def get_replacement_dict():
    """Retrieve dictionary for replacement of game titles."""

    #
    # Manually specify common game abbreviations.
    # Inspiration from: https://boardgamegeek.com/wiki/page/Video_Game_Abbreviations
    #
    abbr_dict = {}

    abbr_dict["7dtd"] = "7 days to die"
    abbr_dict["aoe"] = "age of empires"
    abbr_dict["bg"] = "baldur's gate"
    abbr_dict["bg:soa"] = "baldur's gate ii: shadows of amn"
    abbr_dict["bg: soa"] = "baldur's gate ii: shadows of amn"
    abbr_dict["bg2"] = "baldur's gate ii: shadows of amn"
    abbr_dict["bg:tob"] = "baldur's gate ii: throne of bhaal"
    abbr_dict["bg: tob"] = "baldur's gate ii: throne of bhaal"
    abbr_dict["bg:totsc"] = "baldur's gate: tales of the sword coast"
    abbr_dict["bg: totsc"] = "baldur's gate: tales of the sword coast"
    # "bs", "bs1", and "bs2" omitted due to ambiguity
    abbr_dict["bsi"] = "bioshock infinite"
    abbr_dict["bs3"] = "bioshock infinite"
    abbr_dict["bs 3"] = "bioshock infinite"
    abbr_dict["cod"] = "call of duty"
    abbr_dict["cod:bo"] = "call of duty: black ops"
    abbr_dict["cod: bo"] = "call of duty: black ops"
    abbr_dict["cod:mw2"] = "call of duty: modern warfare 2"
    abbr_dict["cod: mw2"] = "call of duty: modern warfare 2"
    abbr_dict["cod:mw3"] = "call of duty: modern warfare 3"
    abbr_dict["cod: mw3"] = "call of duty: modern warfare 3"
    abbr_dict["coh"] = "company of heroes"
    abbr_dict["csgo"] = "counter-strike: global offensive"
    abbr_dict["cs go"] = "counter-strike: global offensive"
    abbr_dict["cs:go"] = "counter-strike: global offensive"
    abbr_dict["cs: go"] = "counter-strike: global offensive"
    abbr_dict["ct"] = "chrono trigger"
    abbr_dict["dao"] = "dragon age: origins"
    abbr_dict["da2"] = "dragon age: ii"
    abbr_dict["da ii"] = "dragon age: ii"
    abbr_dict["dai"] = "dragon age; inquisition"
    abbr_dict["dah"] = "destroy all humans!"
    abbr_dict["d&d"] = "dungeons & dragons"
    abbr_dict["dnd"] = "dungeons & dragons"
    abbr_dict["dmc"] = "devil may cry"
    abbr_dict["dmc2"] = "devil may cry 2"
    abbr_dict["dmc 2"] = "devil may cry 2"
    abbr_dict["dmc ii"] = "devil may cry 2"
    abbr_dict["dmc3"] = "devil may cry 3: dante's awakening"
    abbr_dict["dmc 3"] = "devil may cry 3: dante's awakening"
    abbr_dict["dmc iii"] = "devil may cry 3: dante's awakening"
    abbr_dict["dmc4"] = "devil may cry 4"
    abbr_dict["dmc 4"] = "devil may cry 4"
    abbr_dict["dmc iv"] = "devil may cry 4"
    abbr_dict["ds"] = "dark souls"
    abbr_dict["ds2"] = "dark souls 2"
    abbr_dict["ds 2"] = "dark souls 2"
    abbr_dict["ds ii"] = "dark souls 2"
    abbr_dict["ds 3"] = "dark souls 3"
    abbr_dict["ds3"] = "dark souls 3"
    abbr_dict["ds iii"] = "dark souls 3"
    # "eso" omitted due to ambiguity
    abbr_dict["ff7"] = "final fantasy vii"
    abbr_dict["ff 7"] = "final fantasy vii"
    abbr_dict["ff vii"] = "final fantasy vii"
    abbr_dict["ff8"] = "final fantasy viii"
    abbr_dict["ff 8"] = "final fantasy viii"
    abbr_dict["ff viii"] = "final fantasy viii"
    abbr_dict["ff9"] = "final fantasy ix"
    abbr_dict["ff 9"] = "final fantasy ix"
    abbr_dict["ff ix"] = "final fantasy ix"
    abbr_dict["fnaf"] = "five nights at freddy's"
    abbr_dict["fnaf2"] = "five nights at freddy's 2"
    abbr_dict["fnaf 2"] = "five nights at freddy's 2"
    abbr_dict["fnaf3"] = "five nights at freddy's 3"
    abbr_dict["fnaf 3"] = "five nights at freddy's 3"
    abbr_dict["fnv"] = "fallout: new vegas"
    abbr_dict["gh"] = "guitar hero"
    # "gow" omitted due to ambiguity
    abbr_dict["gta1"] = "grand theft auto"
    abbr_dict["gta 1"] = "grand theft auto"
    abbr_dict["gta i"] = "grand theft auto"
    abbr_dict["gta2"] = "grand theft auto ii"
    abbr_dict["gta 2"] = "grand theft auto ii"
    abbr_dict["gta ii"] = "grand theft auto ii"
    abbr_dict["gta3"] = "grand theft auto iii"
    abbr_dict["gta 3"] = "grand theft auto iii"
    abbr_dict["gta iii"] = "grand theft auto iii"
    abbr_dict["gta4"] = "grand theft auto iv"
    abbr_dict["gta 4"] = "grand theft auto iv"
    abbr_dict["gta iv"] = "grand theft auto iv"
    abbr_dict["gta5"] = "grand theft auto v"
    abbr_dict["gta 5"] = "grand theft auto v"
    abbr_dict["gta v"] = "grand theft auto v"
    abbr_dict["h1z1"] = "z1 battle royale"
    abbr_dict["hl1"] = "half-life"
    abbr_dict["hl i"] = "half-life"
    abbr_dict["hl2"] = "half-life 2"
    abbr_dict["hl ii"] = "half-life 2"
    abbr_dict["hon"] = "heroes of newerth"
    abbr_dict["ihnmaims"] = "i have no mouth, and i must scream"
    abbr_dict["kcd"] = "kingdom come: deliverance"
    abbr_dict["kh"] = "kingdom hearts"
    abbr_dict["kh i"] = "kingdom hearts"
    abbr_dict["kh 1"] = "kingdom hearts"
    abbr_dict["kh2"] = "kingdom hearts ii"
    abbr_dict["kh 2"] = "kingdom hearts ii"
    abbr_dict["kh ii"] = "kingdom hearts ii"
    abbr_dict["kh3"] = "kingdom hearts iii"
    abbr_dict["kh 3"] = "kingdom hearts iii"
    abbr_dict["kh iii"] = "kingdom hearts iii"
    abbr_dict["lis"] = "life is strange"
    abbr_dict["lltq"] = "long live the queen"
    abbr_dict["loz"] = "the legend of zelda"
    abbr_dict["m&b"] = "mount & blade"
    abbr_dict["mcotd"] = "mordheim: city of the damned"
    abbr_dict["me1"] = "mass effect"
    abbr_dict["me 1"] = "mass effect"
    abbr_dict["me i"] = "mass effect"
    abbr_dict["me2"] = "mass effect 2"
    abbr_dict["me 2"] = "mass effect 2"
    abbr_dict["me ii"] = "mass effect 2"
    abbr_dict["me3"] = "mass effect 3"
    abbr_dict["me 3"] = "mass effect 3"
    abbr_dict["me iii"] = "mass effect 3"
    abbr_dict["mea"] = 'mass effect: andromeda'
    abbr_dict["mgs"] = "metal gear solid"
    abbr_dict["mgs1"] = "metal gear solid"
    abbr_dict["mgs 1"] = "metal gear solid"
    abbr_dict["mgs i"] = "metal gear solid"
    abbr_dict["mgs2"] = "metal gear solid 2: sons of liberty"
    abbr_dict["mgs 2"] = "metal gear solid 2: sons of liberty"
    abbr_dict["mgs ii"] = "metal gear solid 2: sons of liberty"
    abbr_dict["mgs3"] = "metal gear solid 3: snake eater"
    abbr_dict["mgs 3"] = "metal gear solid 3: snake eater"
    abbr_dict["mgs iii"] = "metal gear solid 3: snake eater"
    abbr_dict["mgs4"] = "metal gear solid 4: guns of the patriots"
    abbr_dict["mgs 4"] = "metal gear solid 4: guns of the patriots"
    abbr_dict["mgs iv"] = "metal gear solid 4: guns of the patriots"
    abbr_dict["mtg"] = "magic: the gathering"
    abbr_dict["m:tg"] = "magic: the gathering"
    abbr_dict["m: tg"] = "magic: the gathering"
    abbr_dict["mtgo"] = "magic: the gathering"
    abbr_dict["nms"] = "no man's sky"
    abbr_dict["nwn"] = "neverwinter nights"
    # "poe" omitted due to ambiguity
    abbr_dict["rdr"] = "red dead redemption"
    abbr_dict["re"] = "resident evil"
    abbr_dict["re1"] = "resident evil"
    abbr_dict["re 1"] = "resident evil"
    abbr_dict["re i"] = "resident evil"
    abbr_dict["re2"] = "resident evil 2"
    abbr_dict["re 2"] = "resident evil 2"
    abbr_dict["re ii"] = "resident evil 2"
    abbr_dict["re3"] = "resident evil 3"
    abbr_dict["re 3"] = "resident evil 3"
    abbr_dict["re iii"] = "resident evil 3"
    abbr_dict["re4"] = "resident evil 4"
    abbr_dict["re 4"] = "resident evil 4"
    abbr_dict["re iv"] = "resident evil 4"
    # "som" omitted due to ambiguity
    abbr_dict["sotc"] = "shadow of the colossus"
    abbr_dict["ssz"] = "strike suit zero"
    abbr_dict["tftb"] = "tales from the borderlands"
    abbr_dict["tits"] = "the legend of the heroes: trails in the sky"
    abbr_dict["tlg"] = "the last guardian"
    abbr_dict["tocs"] = "the legend of the heroes: trails of cold steel"
    abbr_dict["tw3"] = "the witcher 3: wild hunt"
    abbr_dict["wow"] = "world of warcraft"
    abbr_dict["zoe"] = "zone of the enders"

    # Additionally, standardize game names for the following
    abbr_dict["dark souls 1"] = "dark souls"
    abbr_dict["dark souls i"] = "dark souls"
    abbr_dict["dark souls ii"] = "dark souls 2"
    abbr_dict["dark souls iii"] = "dark souls 3"
    abbr_dict["final fantasy 7"] = "final fantasy vii"
    abbr_dict["final fantasy 8"] = "final fantasy viii"
    abbr_dict["final fantasy 9"] = "final fantasy ix"
    abbr_dict["grand theft auto 1"] = "grand theft auto"
    abbr_dict["grand theft auto i"] = "grand theft auto"
    abbr_dict["grand theft auto 2"] = "grand theft auto ii"
    abbr_dict["grand theft auto 3"] = "grand theft auto iii"
    abbr_dict["grand theft auto 4"] = "grand theft auto iv"
    abbr_dict["grand theft auto 5"] = "grand theft auto v"
    abbr_dict["half-life 1"] = "half-life"
    abbr_dict["half-life i"] = "half-life"
    abbr_dict["half life 1"] = "half-life"
    abbr_dict["half life i"] = "half-life"
    abbr_dict["half life ii"] = "half-life 2"
    abbr_dict["half-life ii"] = "half-life 2"
    abbr_dict["magic: the gathering online"] = "magic: the gathering"
    abbr_dict["kingdom hearts i"] = "kingdom hearts"
    abbr_dict["kingdom hearts 1"] = "kingdom hearts"
    abbr_dict["kingdom hearts 2"] = "kingdom hearts ii"
    abbr_dict["kingdom hearts 3"] = "kingdom hearts iii"
    abbr_dict["mass effect 1"] = "mass effect"
    abbr_dict["mass effect i"] = "mass effect"
    abbr_dict["mass effect ii"] = "mass effect 2"
    abbr_dict["mass effect iii"] = "mass effect 3"
    abbr_dict["metal gear solid 1"] = "metal gear solid"
    abbr_dict["metal gear solid i"] = "metal gear solid"
    abbr_dict["metal gear solid ii"] = "metal gear solid 2: sons of liberty"
    abbr_dict["metal gear solid 2"] = "metal gear solid 2: sons of liberty"
    abbr_dict["metal gear solid iii"] = "metal gear solid 3: snake eater"
    abbr_dict["metal gear solid 3"] = "metal gear solid 3: snake eater"
    abbr_dict["metal gear solid iv"] = "metal gear solid 4: guns of the patriots"
    abbr_dict["metal gear solid 4"] = "metal gear solid 4: guns of the patriots"
    abbr_dict["resident evil 1"] = "resident evil"
    abbr_dict["resident evil i"] = "resident evil"
    abbr_dict["resident evil ii"] = "resident evil 2"
    abbr_dict["resident evil iii"] = "resident evil 3"
    abbr_dict["resident evil iv"] = "resident evil 4"

    return abbr_dict
