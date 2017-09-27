import requests


class FetchError(Exception): pass

FETCH_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
def fetch(url):
    body = ''
    try:
        resp = requests.get(url, headers={'user-agent': FETCH_USER_AGENT})
        if resp.status_code > 399:
            raise FetchError('Bad server response');
        body = resp.text
    except Exception as e:
        print('HTTP request error: ')
        print(e)
        raise FetchError('Request failed..')

    return body

def normalize(name: str):
    """String normalization is a hairy beast, but we'll make a best effort."""
    name = name.lower()
    tag_index = name.find('|')
    if tag_index >= 0:
        name = name[tag_index+1:]
    name = name.strip()
    name = name.title()
    return name
