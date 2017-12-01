# challonge2csv
A python module to create an excel file showing tournament placings or set records.

##Installation:

Clone or download and extract the repo and do `pip3 install .`

##Usage:

Run standings2csv to generate a table with users as rows, tournaments as columns, and placements as values. records2csv will generate a spreadsheet listing each individual player's record (set wins and losses) against all opponents in the set of tournaments provided.

Note here that callonge_urls.txt is a simple newline delineated list of URLs to the main page of the bracket (e.g., http://gmusmash.challonge.com/bmsmelee22). See sample_tournaments_file.txt for an example.
You will need to obtain your challonge API key: https://challonge.com/settings/developer

Run the commands with no flags or -h to see required and optional parameters. Note if xlsx format is chosen for output the output file name is required. Order of parameters does not matter.

##Examples:

To generate a CSV file from a set of challonge brackets:
`python3 standings2csv.py -u challonge-username -a challonge-api-key -f challonge_urls.txt > output.csv`
or
`python3 standings2csv.py -u challonge-username -a challonge-api-key -f challonge_urls.txt -o output.csv`
or to generate an xlsx:
`python3 standings2csv.py -u challonge-username -a challonge-api-key -f challonge_urls.txt -x -o output.xlsx`

##Notes:

The list of tournaments in the output of standings2csv.py is in the same order they appear in the input file.

Due to python's csv module's incompatability with non-ascii characters on some systems (it appears?) tournaments with player names containing unicode characters may crash the scripts. xlsx mode will work fine.

Some effort is made to normalize player names. Capitalization is ignored, and names with "sponsors" in the form `Team | Player` will count as `player` for the purpose of recording results. If players use multiple names throughout the season the script will just identify them as multiple players.

##TODO:

-put in PyPI

-alphabetize list of opponents in records2csv output

-remove duplicates from list of tournaments, if user shall be silly enough to do so

-replace the csv writer with one that can handle unicode

-(xlsx) use colors for good placements in standings, and green/red/yellow for winning/losing/mixed records against certain opponents in records

-(xlsx) link to tournaments for the entries in row 1 of standings (should be easy)

-(xlsx) annotate cells with multiple links to tournaments/matches in which wins/losses to that player happened in records (should be hard, will require modifying internal data structures)
