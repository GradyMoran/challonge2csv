# challonge2csv
A python module to create an excel file showing tournament placings.

#Installation:

Clone the repo and do `pip3 install .`
In the future this can go onto PyPI for easy installation.

#Usage:

(Note here that callonge_urls.txt is a simple newline delineated list of URLs.)

## challonge2csv
To Generate a CSV file from a set of challonge brackets:
`standings2csv challonge_urls.txt > output.csv`


## player_records2csv
A python script to create an excel file showing wins and losses for each player.

Usage:
records2csv.py challonge_urls.txt > output.csv

challonge_urls.txt is a text file with one tournament url per line. Each url needs to be to the main page of the bracket (e.g. http://gmusmash.challonge.com/bmsmelee22). See sample_tournaments_file.txt for an example.

TODO:

-make some decision about case sensitivity- should "Tape" and "tape" be considered the same player?

-output an xlsx instead of a csv with pretty colors and formatting
