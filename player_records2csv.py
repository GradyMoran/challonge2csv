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

	season_sets = list()
	player_list = list()
	for line in f:
		html_file = urllib.request.urlretrieve(line)[0]
		with open(html_file, 'r') as t:
			html_data=t.read()

		record_js_strings = re.findall(r'tournament_id[^{]*{[^{]*{[^{]*{', html_data) #that re is stupid
		for s in record_js_strings:
			#print("\n\n" + s)
			tmp_players = re.findall(r'display_name":"[^"]*', s)
			for i in range(0,len(tmp_players)):
				tmp_players[i] = tmp_players[i][15:]
			#print(tmp_players)
			score = re.findall(r'scores":[^\]]*]', s)[0]
			#print(score[8:])
			gc1 = int(re.split(',', score[8:][1:])[0])
			gc2 = int(re.split(',', score[8:][:-1])[1])
			#print ("wgc: " + str(wgc) + " lgc: " + str(lgc))
			if gc2 > gc1:
				gc1, gc2 = gc2, gc1
				tmp_players[0], tmp_players[1] = tmp_players[1], tmp_players[0]
			#print(tmp_players)
			#print ("wgc: " + str(gc1) + " lgc: " + str(gc2))
			season_sets.append(Set(winner=tmp_players[0], loser=tmp_players[1]))

#	for s in season_sets:
#		print(str(s))

	for s in season_sets:
		player_list.append(s[0])
		player_list.append(s[1])

	player_list = list(set(player_list))
	player_list = sorted(player_list, key=str.lower)

#	print(player_list)
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
"""
#challonge doesn't like urllib's default user agent header
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

with open(sys.argv[1]) as f:
	
	for line in f:
		html_file = urllib.request.urlretrieve(line)[0]
		with open(html_file, 'r') as t:
			html_data=t.read().replace('\n','')

		ranks = re.findall(r'<td class=.rank. rowspan=.[0-9]*..[0-9]*', html_data)
		for i in range(0,len(ranks)):
			k = ranks[i].rfind(">")
			ranks[i] = int(ranks[i][k+1:])
		ranks.append(99999) #this makes my rank determining logic below work. fix if you think of a better way to do it

		players = re.findall(r'<span>[^<]*</span>', html_data)
		for i in range(0,len(players)):
			players[i] = players[i][6:-7]

		player_count = 0
		current_rank_index = 0
		tmpdict = {}
		for player in players:
			player_count+=1
			if player_count >= ranks[current_rank_index+1]:
				current_rank_index+=1
			tmpdict[player]=ranks[current_rank_index]

		tournament_results.append(tmpdict)

	#get list of all players, sorted without duplicates
	all_players = list()
	for d in tournament_results:
		all_players = all_players + list(d.keys())
	all_players = list(set(all_players))
	all_players = sorted(all_players, key=str.lower)

	#outputting the tournaments to top line
	print(",", end="")
	for t in tournament_names:
		print(t + ",", end="")
	print()

	#outputting players and their results
	for p in all_players:
		print(p + ",", end="")
		for i in range(0, len(tournament_results)):
			if p in tournament_results[i]:
				print(str(tournament_results[i].get(p)) + ",", end="")
			else:
				print(",", end="")
		print()
"""
