#!/usr/bin/python3
import argparse
import challonge
import csv
import re
import sys
import xlsxwriter

from collections import namedtuple
from challonge2csv.utils import normalize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help="Your challonge username. Does not need to be the same user who created the tournament(s)")
    parser.add_argument('-a', '--api_key', required=True, help="Your challonge API key. Can be obtained from https://challonge.com/settings/developer")
    parser.add_argument('-f', '--tournaments_file', required=True, help="A file containing URLs to the challonge tournaments to include, one URL per line.")
    parser.add_argument('-x', '--xlsx', required=False, help="Create an xlsx instead. Requires an output file to be specified", action='store_true')
    parser.add_argument('-o', '--output_file', required=False, help="Name of file to output. Required for xlsx. csv will default to stdout.")
    args = parser.parse_args()

    if (args.xlsx and args.output_file is None):
        raise Exception("If output file type is xlsx an output file must be specified.")

    (players, season_records) = gen_records(args.username, args.api_key, args.tournaments_file)
    
    if (args.xlsx):
        output_xlsx(players, season_records, args.output_file)#xlsxwriter wants a file name, not a handle.
    else:
        if (args.output_file is not None):
            f = open(args.output_file, "w+")
            output_csv(players, season_records, f)
            f.close()
        else:
            output_csv(players, season_records, sys.stdout)

def gen_records(username: str, api_key: str, tournaments_file: str):
    with open(tournaments_file, 'r') as f:
        tournaments=f.read()

    return gen_records_from_str(username, api_key, tournaments)

def gen_records_from_str(username: str, api_key: str, tournaments: str):  
    challonge.set_credentials(username, api_key)
    
    # Define our set named tuples
    Set = namedtuple("Set", "winner loser t_url")

    player_list = set()

    season_sets = list() #season sets is a list of (winner,loser, url) tuples. There is one tuple per set, for each set in the list of urls provided.
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
        player_list.update(player_ids.values())
        
        for match in matches:
            winner = player_ids[match['winner_id']]
            loser = player_ids[match['loser_id']]
            season_sets.append(Set(winner=winner, loser=loser, t_url=url))

    player_list = sorted(player_list, key=str.lower)

    # Initialize an empty record for each player.
    # A record is a defined as a dict mapping a player name to a 2-tuple of 2-tuple: ((wins, [tourney_urls]),(losses, [tourney_urls]))
    #  Player Name =>
    #    - Player 2 Name =>
    #      - Wins, URLs of tournaments
    #      - Losses, URLs of tournaments
    #
    # Using this format makes our data manipulation and walking very simple.

    season_records = {}
    for p in player_list:
        season_records[p] = {}
        for p2 in player_list:
            if p2 == p:
                continue
            season_records[p][p2] = [[0,[]], [0, []]]

    for s in season_sets:
        w, l, u = s
        season_records[w][l][0][0] += 1
        season_records[w][l][0][1].append(u) #Is it possible to efficently sort as they're inserted?
        season_records[l][w][1][0] += 1
        season_records[l][w][1][1].append(u)
        
    return (player_list, season_records)
        
def output_csv(players, season_records, output_file):
    writer = csv.writer(output_file)
    for player in players:
        writer.writerow([player])
        writer.writerow(["Player:", "Wins:", "Losses:"])

        for player2 in sorted(season_records[player].keys()):
            record = season_records[player][player2]

            # We want to prune players who never played.
            if record[0][0] > 0 or record[1][0] > 0:
                writer.writerow([player2, record[0][0], record[1][0]])

        writer.writerow([])

def output_xlsx(players, season_records, output_filename):
    wb = xlsxwriter.Workbook(output_filename)
    ws = wb.add_worksheet()
    r = 0
    for player in players:
        ws.write(r, 0, player)
        r+=1
        ws.write_row(r, 0, ["Player:", "Wins:", "Losses:"])
        r+=1
        for player2 in sorted(season_records[player].keys()):
            record = season_records[player][player2]

            # We want to prune players who never played.
            if record[0][0] > 0 or record[1][0] > 0:
                ws.write_row(r, 0, [player2, record[0][0], record[1][0]])
                if (len(record[0][1]) > 0):
                    ws.write_comment(r, 1, '\n'.join(record[0][1]), {'x_scale': 2})
                if (len(record[1][1]) > 0):
                    ws.write_comment(r, 2, '\n'.join(record[1][1]), {'x_scale': 2})
                r+=1
        r+=1
    wb.close()      

if __name__ == '__main__':
    main()
