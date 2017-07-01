# challonge2csv
Bash script to create an excel file showing tournament placings given a file of urls to challonge standings

Usage:
./challonge2csv.bash challonge_standings_urls.txt > output.csv
challonge_standings_urls.txt needs urls formatted like http://gmusmash.challonge.com/bmsmelee22/standings with the 'standings' part at the end.

TODO:
add capability of putting multiple tournaments in input file
add top row with tournament urls
add capability of showing losses and wins for any given player
