#!/usr/bin/python3
import argparse
import challonge
import re
import sys
import math

from collections import namedtuple
from challonge2csv.utils import normalize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help="Your challonge username. Does not need to be the same user who created the tournament(s)")
    parser.add_argument('-a', '--api_key', required=True, help="Your challonge API key. Can be obtained from https://challonge.com/settings/developer")
    parser.add_argument('-f', '--tournaments_file', required=True, help="A file containing URLs to the challonge tournaments to include, one URL per line.")
    args = parser.parse_args()

    for line in conflicts(old_matchups, new_matchups):
        print(line)

def new_matchups_from_str(username: str, api_key: str, url: str):
    #so the top n players get a bye, where n is the smallest number s.t. n+t=2^k, where t is the toal number of players, and k is an integer. Or if n = 0, everyone fights in round one.
    subdomain = url[url.find("//")+2:url.find(".")]
    tourney_name = url[url.rfind("/")+1:]
    if subdomain == "challonge":
        query = tourney_name
    else:
        query = subdomain + "-" + tourney_name     

    participants = []
    #make list of participants ordered by seed (which is order api returns)
    for participant in challonge.participants.index(query): #doesn't like this
        participants.append(participant['name'])

    round_one_participants = len(participant_seeds) - stupid_func(len(participant_seeds))

    round_one_matchups = set()
    round_one_players = round_one_participants[(-1*round_one_participants):]
    i = 0 
    j = len(round_one_players)
    while i < j:
        round_one_matchups.add(frozenset([round_one_players[i], round_one_players[j]]))

    return round_one_matchups

#find smallest n s.t. n+t is a power of 2
def stupid_func(t):
    n = 0
    while bin(n+t).count('1') != 1:
        n += 1

    return n

def old_matchups(username: str, api_key: str, tournaments_file: str):
    with open(tournaments_file, 'r') as f:
        tournaments = f.read()

    return old_matchups_from_str(username, api_key, tournaments_file)

def old_matchups_from_str(username: str, api_key: str, tournaments: str):
    challonge.set_credentials(username, api_key)

    old_matches = set() #set of tuples of (players set, date string)
    print(type(old_matches))
    for line in tournaments.split('\n'):
        url = line.strip()
        if url == "":
            continue

        #get the query for challonge API from the user's provided urls
        subdomain = url[url.find("//")+2:url.find(".")]
        tourney_name = url[url.rfind("/")+1:]
        if subdomain == "challonge":
            query = tourney_name
        else:
            query = subdomain + "-" + tourney_name
        participants = challonge.participants.index(query)
        matches = challonge.matches.index(query)
        
        #create a map of player_id->name since the matches structure below identifies players by their id, not name.
        player_ids = {}
        for participant in participants:
            name = participant['name']
            player_id = participant['id']
            player_ids[player_id] = normalize(name)

        for match in matches:
            old_matches.add((frozenset([player_ids[match['player1_id']], player_ids[match['player2_id']]]), match['started_at'].strftime("%b %d, %Y")))

    return old_matches
   
if __name__ == '__main__':
    main()
