def normalize(name: str):
    """String normalization is a hairy beast, but we'll make a best effort."""
    name = name.lower()
    tag_index = name.find('|')
    if tag_index >= 0:
        name = name[tag_index+1:]
    name = name.strip()
    name = name.title()
    return name

#input: string containing one tournament url per line
#output: 3-tuple of list of tournament urls with duplicates removed (as defined by two leading to the same tournament, i.e. two urls are duplicates iff their names are the same), tournament queries (e.g., gmusmash-bmsmelee22), and tournament short names (e.g., bmsmelee22). All lists guaranteed to be the same size and contain no duplicates and be in the same order as shown in tournament_urls
def normalize_urls(tournament_urls: str):
    final_urls = []
    final_queries=[]
    final_names = []
    for line in tournament_urls.split('\n'):
        url = line.strip()
        if url == "":
            continue
        #get the query for challonge API from the user's provided urls
        subdomain = url[url.find("//")+2:url.find(".")]
        tourney_name = url[url.rfind("/")+1:]
        if subdomain == "challonge":
            query = tourney_name
        else:
            query = subdomain + "-" + tourney_name

        if query in final_names:
            continue
        else:
            final_urls.append(url)
            final_queries.append(query)
            final_names.append(tourney_name)

    return (final_urls, final_queries, final_names)
