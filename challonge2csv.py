#!/usr/bin/python3
import csv
import re
import sys
import urllib.request

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

with open(sys.argv[1]) as f:
	tournament_results = []
	tournament_names = []
	for line in f:
		tournament_names.append(line)
		html_file = urllib.request.urlretrieve(line)[0]
		with open(html_file, 'r') as t:
			html_data=t.read().replace('\n','')

		ranks = re.findall(r'<td class=.rank. rowspan=.[0-9]*..[0-9]*', html_data)
		for i in range(0,len(ranks)):
			k = ranks[i].rfind(">")
			ranks[i] = int(ranks[i][k+1:])
		ranks.append(99999)

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

	#get list of all players
	all_players = list()
	for d in tournament_results:
		all_players = all_players + list(d.keys())
	all_players = list(set(all_players))
	all_players = sorted(all_players, key=str.lower)

	#outputting the tournaments to top line
	print(",", end="")
	for t in tournament_names:
		print(t.replace('\n','') + ",", end="")
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
