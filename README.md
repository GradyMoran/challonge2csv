# challonge2csv
A python module to create an excel file showing tournament placings.

#Installation:

Clone the repo and do `pip3 install .`

#Usage:

Note here that callonge_urls.txt is a simple newline delineated list of URLs.
You will need to obtain your challonge API key: https://challonge.com/settings/developer

challonge_urls.txt is a text file with one tournament url per line. Each url needs to be to the main page of the bracket (e.g. http://gmusmash.challonge.com/bmsmelee22). See sample_tournaments_file.txt for an example.

## challonge2csv
To Generate a CSV file from a set of challonge brackets:
`python3 standings2csv.py -u challonge-username -a challonge-api-key -f challonge_urls.txt > output.csv`


## records2csv
A python script to create an excel file showing wins and losses for each player.
`python3 records2csv.py -u challonge-username -a challonge-api-key -f challonge_urls.txt > output.csv`

xlsx files can also be created. Run the scripts and see the help dialogs.

TODO:

-put in PyPI

-(xlsx) use colors for good placements in standings, and green/red/yellow for winning/losing/mixed records against certain opponents in records

-(xlsx) link to tournaments for the entries in row 1 of standings (should be easy)

-(xlsx) is it possible to annotate a cell with multiple links to tournaments/matches(if possible?) in which wins/losses to that player happened in records? (should be hard)
