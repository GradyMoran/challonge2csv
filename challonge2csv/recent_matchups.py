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
    parser.add_argument('-p', '--previous_tournaments', required=True, help="A comma-separated string of previous tournaments to look for conflicting matchups in")
    parser.add_argument('-n', '--new_tournament', required=True, help="The URL of the new tournament")
    args = parser.parse_args()

    #todo, parse the csv of previous tournaments
    old_matchups = old_matchups_from_str(args.username, args.api_key, args.previous_tournaments)
    new_matchups = new_matchups_from_str(args.username, args.api_key, args.new_tournament)
    print("new_matchups: ")
    print(new_matchups)
    print(old_matchups)

    c = 0
    for line in conflicts(old_matchups, new_matchups):
        c += 1
        print(line)

    if c == 0:
        print("No conflicts.")

def new_matchups_from_str(username: str, api_key: str, url: str):
    challonge.set_credentials(username, api_key)
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

    round_one_participants = len(participants) - stupid_func(len(participants))

    round_one_matchups = set()
    round_one_players = participants[(-1*round_one_participants):]
    i = 0 
    j = len(round_one_players)-1
    while i < j:
        player_one = normalize(round_one_players[i])
        player_two = normalize(round_one_players[j])
        if player_two < player_one:
            player_one, player_two = player_two, player_one
        round_one_matchups.add(frozenset([player_one, player_two]))
        i+=1
        j-=1

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
    #print(type(old_matches))
    #for line in tournaments.split('\n'):
    for line in tournaments.split(','):
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
        tmp_tournament = challonge.tournaments.show(query)
        match_date = tmp_tournament['started_at'].strftime("%b %d, %Y")
        participants = challonge.participants.index(query)
        matches = challonge.matches.index(query)
        
        #create a map of player_id->name since the matches structure below identifies players by their id, not name.
        player_ids = {}
        for participant in participants:
            name = participant['name']
            player_id = participant['id']
            player_ids[player_id] = normalize(name)

        for match in matches:
            #print(match)
            #old_matches.add((frozenset([player_ids[match['player1_id']], player_ids[match['player2_id']]]), match['started_at'].strftime("%b %d, %Y")))
            player_one = normalize(player_ids[match['player1_id']])
            player_two = normalize(player_ids[match['player2_id']])
            if player_two < player_one:
                player_one, player_two = player_two, player_one 
            old_matches.add((frozenset([player_one, player_two]), match_date))


    return old_matches

def conflicts(old_matches, new_matches):
    ret = []
    for omatch in old_matches:
        for nmatch in new_matches:
            if omatch[0] == nmatch:
                tmp = list(nmatch)
                ret.append("conflict: " + tmp[0] + " played " + tmp[1] + " on " + omatch[1])
    return ret
 
if __name__ == '__main__':
    main()
