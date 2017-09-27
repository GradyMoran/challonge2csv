#!/usr/bin/python3
import csv
import json
import re
import sys
from collections import namedtuple

from challonge2csv.utils import fetch, normalize


def main():
    # Define our set named tuples
    Set = namedtuple("Set", "winner loser")

    # Regex to pull out the main data object challonge stores on the page.
    json_finder = re.compile(r'\[["\']TournamentStore[\'"]\] ?= ?({.*?});')
    player_list = set()

    season_sets = list() #season sets is a list of (winner,loser) tuples. There is one tuple per set, for each set in the list of urls provided.
    with open(sys.argv[1]) as f:
        for line in f:
            html_body = fetch(line.strip())

            # Use this to have a real python dict to walk through rather than regexing into it repeatedly.
            # In standings we can just html parse, but to find the js object in the JS, we have no choice but
            # to use a regex.
            tourney = json_finder.search(html_body, re.MULTILINE).group(1)
            tourney = json.loads(tourney)

            # This just flattens the rounds out. List comprehension reference: https://stackoverflow.com/a/9061815
            matches = [match for rnd in tourney['matches_by_round'].values() for match in rnd]


            for match in matches:
                tmp_players = [match['player1']['display_name'], match['player2']['display_name']]
                tmp_players = list(map(normalize, tmp_players))
                player_list.update(tmp_players)
                gc1, gc2 = match['scores']

                # Winner goes first
                if gc2 > gc1:
                    gc1, gc2 = gc2, gc1
                    tmp_players[0], tmp_players[1] = tmp_players[1], tmp_players[0]
                season_sets.append(Set(winner=tmp_players[0], loser=tmp_players[1]))

    player_list = sorted(player_list, key=str.lower)

    # Initialize an empty record for each player.
    # A record is a defined as a dict mapping a player name to a 2-tuple of wins/losses
    #
    #  Player Name =>
    #    - Player 2 Name =>
    #      - Wins
    #      - Losses
    #
    # Using this format makes our data manipulation and walking very simple.

    season_records = {}
    for p in player_list:
        season_records[p] = {}
        for p2 in player_list:
            if p2 == p:
                continue
            season_records[p][p2] = [0, 0]

    for s in season_sets:
        w, l = s
        season_records[w][l][0] += 1
        season_records[l][w][1] += 1

    writer = csv.writer(sys.stdout)
    for player in player_list:
        writer.writerow([player])
        writer.writerow(["player", "wins", "losses"])

        for player2 in season_records[player].keys():
            record = season_records[player][player2]

            # We want to prune players who never played.
            if record[0] > 0 or record[1] > 0:
                writer.writerow([player2] + season_records[player][player2])

        writer.writerow([])

if __name__ == '__main__':
    main()
