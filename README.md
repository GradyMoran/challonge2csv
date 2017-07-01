# challonge2csv
A python script to create an excel file showing tournament placings.

Usage:
python3 challonge2csv.py challonge_urls.txt > output.csv

challonge_standings_urls.txt is a text file with one tournament url per line. Each url needs to be to the main page of the bracket (e.g. http://gmusmash.challonge.com/bmsmelee22)

TODO:
possibly export as an xlsx instead with better column width, colors highlighting good/bad placements, and other eye candy
add capability of showing losses and wins for any given player
