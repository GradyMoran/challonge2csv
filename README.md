# challonge2csv
A python script to create an excel file showing tournament placings.

Usage:
python3 challonge2csv.py challonge_urls.txt > output.csv

# player_records2csv
A python script to create an excel file showing wins and losses for each player.

Usage:
python3 player_records2csv.py challonge_urls.txt > output.csv

challonge_urls.txt is a text file with one tournament url per line. Each url needs to be to the main page of the bracket (e.g. http://gmusmash.challonge.com/bmsmelee22). See sample_tournaments_file.txt for an example.

TODO:
-make some decision about case sensitivity- should "Tape" and "tape" be considered the same player?
-output an xlsx instead of a csv with pretty colors and formatting
-do it "the right way" with an xml parser or some advanced technology instead of a regular expression on the html
