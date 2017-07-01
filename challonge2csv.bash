#!/bin/bash

player_count=0
tournament_count=0
current_rank_index=0

while read line; do
	page_contents=$(curl -s $line)
	players=$(echo "$page_contents" | grep -o -e "<span>[^<]*..span>" | sed 's/\r/NEWLINE/g' | sed -r 's/<span>|<\/span>//g') #get list of players from challonge html
	ranks_string=$(echo "$page_contents" | grep -o -e "<td class=.rank. rowspan=.[0-9]*..[0-9]*" | sed 's/.*>//g') #get list of ranks players achieved in that tournament from challonge html (1,2,3,4,5,7,9,11...)
	IFS=' ' read -r -a ranks <<< $ranks_string
	ranks["${#ranks[@]}"]=99999 #put in a placing worse than anybody could possibly get at the end of the ranks array... helps with logic below

	while read -r player; do
		player_count=$(($player_count + 1))
		if [ "$player_count" -ge "${ranks[$(($current_rank_index + 1))]}" ]; then
			current_rank_index=$(($current_rank_index + 1))
		fi

		echo "$player,${ranks[$current_rank_index]}" #this step is going to have to change a lot to add support for multiple tournaments, since each tournament gets a column, and each player gets only one row

	done <<< "$players"
done <$1
