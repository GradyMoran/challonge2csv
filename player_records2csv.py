#!/usr/bin/python3
import re
import sys
import urllib.request

from collections import namedtuple

#define our set named tuples
Set = namedtuple("Set", "winner loser")

#challonge doesn't like urllib's default user agent header
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

with open(sys.argv[1]) as f:

	season_sets = list() #season sets is a list of (winner,loser) tuples. There is one tuple per set, for each set in the list of urls provided.
	for line in f:
		html_file = urllib.request.urlretrieve(line)[0]
		with open(html_file, 'r') as t:
			html_data=t.read()

		#each string is a set
		record_js_strings = re.findall(r'tournament_id[^{]*{[^{]*{[^{]*{', html_data) #that regex is stupid
		for s in record_js_strings:
			#get player names
			tmp_players = re.findall(r'display_name":"[^"]*', s)
			for i in range(0,len(tmp_players)):
				tmp_players[i] = tmp_players[i][15:]
			#get set game counts
			score = re.findall(r'scores":[^\]]*]', s)[0]
			gc1 = int(re.split(',', score[8:][1:])[0])
			gc2 = int(re.split(',', score[8:][:-1])[1])
			if gc2 > gc1:
				gc1, gc2 = gc2, gc1
				tmp_players[0], tmp_players[1] = tmp_players[1], tmp_players[0]
			season_sets.append(Set(winner=tmp_players[0], loser=tmp_players[1]))

	#make the sorted list of all players that participated this season
	player_list = list()
	for s in season_sets:
		player_list.append(s[0])
		player_list.append(s[1])
	player_list = list(set(player_list))
	player_list = sorted(player_list, key=str.lower)

	season_records = list() #season records is a list of tuples. each tuple contains three values: player name, wins (dict of player name keys and set count values), and losses (another dict of player name keys and set count values)
	for p in player_list:
		tmp_tuple = (p,{},{})
		season_records.append(tmp_tuple)

	for s in season_sets:
		w = s[0]
		l = s[1]
		for r in season_records:
			#update the winner's season record
			if r[0] == w:
				if l in r[1]:
					r[1][l] = r[1][l]+1
				else:
					r[1][l] = 1
			#update loser's
			if r[0] == l:
				if w in r[2]:
					r[2][w] = r[2][w]+1
				else:
					r[2][w] = 1

	#printing to csv
	for r in season_records:
		print(r[0])
		print("wins,,losses")
		print("player,set count,player,set count")
		w_iter = iter(r[1])
		l_iter = iter(r[2])
		for i in range(0,min(len(r[1]),len(r[2]))):
			tmp_win = next(w_iter)
			tmp_loss = next(l_iter)
			print(tmp_win + "," + str(r[1][tmp_win]) + "," + tmp_loss + "," + str(r[2][tmp_loss]))
		for i in range(len(r[2]), len(r[1])): #more wins than losses
			tmp_win = next(w_iter)
			print(tmp_win + "," + str(r[1][tmp_win]))
		for i in range(len(r[1]), len(r[2])): #more losses than wins
			tmp_loss = next(l_iter)
			print(",," + tmp_loss + "," + str(r[2][tmp_loss]))
		print()
