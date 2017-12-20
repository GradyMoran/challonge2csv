#!/usr/bin/python3
import argparse
import challonge
import csv
import sys
import xlsxwriter
 
from challonge2csv.utils import normalize_urls, normalize
 
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

    with open(args.tournaments_file, 'r') as f:
        tournaments=f.read()

    (players, tournament_results, tournament_urls, tournament_names) = gen_standings(args.username, args.api_key, tournaments)

    if (args.xlsx):
        output_xlsx(players, tournament_results, tournament_names, tournament_urls, args.output_file)#xlsxwriter wants a file name, not a handle.
    else:
        if (args.output_file is not None):
            f = open(args.output_file, "w+")
            output_csv(players, tournament_results, tournament_names, f)
            f.close()
        else:
            output_csv(players, tournament_results, tournament_names, sys.stdout)

#returns tuple of players (list), tournament_results (list of dicts of name keys and rank values. one dict per tournament), tournament_urls (list), tournament_names (list)
#in this case, tournaments is a multiline string corresponding to the contents of the input file.
def gen_standings(username: str, api_key: str, tournaments: str):
    challonge.set_credentials(username, api_key)
    tournament_results = []
    (tournament_urls, tournament_queries, tournament_names) = normalize_urls(tournaments)
    for query in tournament_queries:
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
 
    return (players, tournament_results, tournament_urls, tournament_names)

#output_csv takes a handle as an argument, which allows you to write to either stdout or a file easily.
def output_csv(players, tournament_results, tournament_names, output_file):
    writer = csv.writer(output_file)
    writer.writerow([None] + tournament_names)
    for p in players:
        row = [p] + list(map(lambda tourney: tourney.get(p), tournament_results))
        writer.writerow(row)
        
#xlsx takes a filename as an argument, since you can't initialize an xlsxwriter with a handle.
def output_xlsx(players, tournament_results, tournament_names, tournament_urls, output_filename):
    wb = xlsxwriter.Workbook(output_filename)
    bronze = wb.add_format()
    bronze.set_bg_color("#8C7853")
    silver = wb.add_format()
    silver.set_bg_color("#808080")
    gold = wb.add_format()
    gold.set_bg_color("#CFB53B")
    ws = wb.add_worksheet()

    for i in range(len(tournament_names)):
        ws.write_url(0, i+1, tournament_urls[i], string=tournament_names[i])
    r = 1
    for p in players:
        ws.write(r, 0, p)
        row = list(map(lambda tourney: tourney.get(p), tournament_results))
        for i in range(len(row)):
            if row[i] == 1:
                ws.write(r, i+1, row[i], gold)
            elif row[i] == 2:
                ws.write(r, i+1, row[i], silver)
            elif row[i] == 3:
                ws.write(r, i+1, row[i], bronze)
            else:
                ws.write(r, i+1, row[i])
        r+=1
    wb.close()

if __name__ == '__main__':
    main()
