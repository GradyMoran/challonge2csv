#!/usr/bin/python3
import argparse
import challonge
import csv
import sys
import xlsxwriter
 
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

    (players, tournament_results, tournament_names) = gen_standings(args.username, args.api_key, args.tournaments_file)

    if (args.xlsx):
        output_xlsx(players, tournament_results, tournament_names, args.output_file)#xlsxwriter wants a file name, not a handle.
    else:
        if (args.output_file is not None):
            f = open(args.output_file, "w+")
            output_csv(players, tournament_results, tournament_names, f)
            f.close()
        else:
            output_csv(players, tournament_results, tournament_names, sys.stdout)

#returns tuple of players (list), tournament_results (dict), tournament_names (list)
def gen_standings(username: str, api_key: str, tournaments_file: str):
    with open(tournaments_file, 'r') as f:
        tournaments=f.read()

    return gen_standings_from_str(username, api_key, tournaments)

#returns tuple of players (list), tournament_results (dict), tournament_names (list)
#in this case, tournaments is a multiline string corresponding to the contents of the input file.
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
 
    return (players, tournament_results, tournament_names)

#output_csv takes a handle as an argument, which allows you to write to either stdout or a file easily.
def output_csv(players, tournament_results, tournament_names, output_file):
    writer = csv.writer(output_file)
    writer.writerow([None] + tournament_names)
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournament_results))
        writer.writerow(row)
        
#xlsx takes a filename as an argument, since you can't initialize an xlsxwriter with a handle.
def output_xlsx(players, tournament_results, tournament_names, output_filename):
    wb = xlsxwriter.Workbook(output_filename)
    ws = wb.add_worksheet()
    ws.write_row(0, 0, [None] + tournament_names)
    r = 1
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournament_results))
        ws.write_row(r, 0, row)
        r+=1
    wb.close()
 
if __name__ == '__main__':
    main()
