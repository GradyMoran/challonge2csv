#!/usr/bin/python3
 
import string
import challonge
import csv
import sys
import argparse
 
from challonge2csv.utils import fetch, normalize
 
tournament_results = []
tournament_names = []
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help="Your challonge username. Does not need to be the same user who created the tournament(s)")
    parser.add_argument('-a', '--api_key', required=True, help="Your challonge API key. Can be obtained from https://challonge.com/settings/developer")
    parser.add_argument('-f', '--tournaments_file', required=True, help="A file containing URLs to the challonge tournaments to include, one URL per line.")
    args = parser.parse_args()

    challonge.set_credentials(args.username, args.api_key)
    with open(args.tournaments_file) as f:
        for line in f:
            url = line.strip()
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
 
    print_results(players, tournament_results)
 
def print_results(players, tournaments):
    writer = csv.writer(sys.stdout)
    writer.writerow([None] + tournament_names)
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournaments))
        writer.writerow(row)
 
if __name__ == '__main__':
    main()
