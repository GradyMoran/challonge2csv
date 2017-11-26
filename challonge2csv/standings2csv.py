#!/usr/bin/python3
 
import string
import challonge
import csv
import sys
import argparse
 
from challonge2csv.utils import fetch, normalize
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help="Your challonge username. Does not need to be the same user who created the tournament(s)")
    parser.add_argument('-a', '--api_key', required=True, help="Your challonge API key. Can be obtained from https://challonge.com/settings/developer")
    parser.add_argument('-f', '--tournaments_file', required=True, help="A file containing URLs to the challonge tournaments to include, one URL per line.")
    args = parser.parse_args()

    gen_standings(args.username, args.api_key, args.tournaments_file)

def gen_standings(username: str, api_key: str, tournaments_file: str):
    with open(tournaments_file, 'r') as f:
        tournaments=f.read()

    gen_standings_from_str(username, api_key, tournaments)

def gen_standings_from_str(username: str, api_key: str, tournaments: str):
    challonge.set_credentials(username, api_key)
    tournament_results = []
    tournament_names = []

    for line in tournaments.split('\n'):
        url = line.strip()
        if url == "":
            continue
        
        #get the query for challonge API from the user's provided urls
        subdomain = url[url.find("//")+2:url.find(".")]
        tourney_name = url[url.rfind("/")+1:]
        tournament_names.append(tourney_name)
        if subdomain == "challonge":
            query = tourney_name
        else:
            query = subdomain + "-" + tourney_name
        participants = challonge.participants.index(query)

        results = {}
        for participant in participants:
            name = participant['name']
            rank = participant['final_rank']
            results[normalize(name)] = rank

        tournament_results.append(results)

   
    players = set()
    for t in tournament_results:
        players.update(t.keys())
    players = sorted(players)
 
    print_results(players, tournament_results, tournament_names)
 
def print_results(players, tournament_results, tournament_names):
    writer = csv.writer(sys.stdout)
    writer.writerow([None] + tournament_names)
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournament_results))
        writer.writerow(row)
 
if __name__ == '__main__':
    main()
