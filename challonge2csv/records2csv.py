#!/usr/bin/python3
import csv
import json
import re
import sys
import argparse
import challonge
from collections import namedtuple

from challonge2csv.utils import fetch, normalize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help="Your challonge username. Does not need to be the same user who created the tournament(s)")
    parser.add_argument('-a', '--api_key', required=True, help="Your challonge API key. Can be obtained from https://challonge.com/settings/developer")
    parser.add_argument('-f', '--tournaments_file', required=True, help="A file containing URLs to the challonge tournaments to include, one URL per line.")
    args = parser.parse_args()
    
    challonge.set_credentials(args.username, args.api_key)
    
    # Define our set named tuples
    Set = namedtuple("Set", "winner loser")

    player_list = set()

    season_sets = list() #season sets is a list of (winner,loser) tuples. There is one tuple per set, for each set in the list of urls provided.
    with open(args.tournaments_file) as f:
        for line in f:
            url = line.strip()

            # Use this to have a real python dict to walk through rather than regexing into it repeatedly.
            # In standings we can just html parse, but to find the js object in the JS, we have no choice but
            # to use a regex.
            subdomain = url[url.find("//")+2:url.find(".")]
            tourney_name = url[url.rfind("/")+1:]
            if subdomain == "challonge":
                query = tourney_name
            else:
                query = subdomain + "-" + tourney_name
            #tournament = challonge.tournaments.show(query)
            participants = challonge.participants.index(query)
            matches = challonge.matches.index(query)
            
            #create a map of player_id->name since the matches structure below identifies players by their id, not name.
            player_ids = {}
            for participant in participants:
                name = participant['name']
                player_id = participant['id']
                player_ids[player_id] = normalize(name)
            player_list.update(player_ids.values())
            
            for match in matches:
                winner = player_ids[match['winner_id']]
                loser = player_ids[match['loser_id']]
                season_sets.append(Set(winner=winner, loser=loser))

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
        writer.writerow(["Player:", "Wins:", "Losses:"])

        for player2 in season_records[player].keys():
            record = season_records[player][player2]

            # We want to prune players who never played.
            if record[0] > 0 or record[1] > 0:
                writer.writerow([player2] + season_records[player][player2])

        writer.writerow([])
        

if __name__ == '__main__':
    main()
