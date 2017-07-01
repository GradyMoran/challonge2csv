# challonge2csv
A bash script to create an excel file showing tournament placings.

Usage:
./challonge2csv.bash challonge_standings_urls.txt > output.csv

challonge_standings_urls.txt is a text file with one url per line. Each url needs to be to the /standings/ page of the bracket (e.g. http://gmusmash.challonge.com/bmsmelee22/standings)

TODO:
add capability of putting multiple tournaments in input file
add top row with tournament urls
add capability of showing losses and wins for any given player
