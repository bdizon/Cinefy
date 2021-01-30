import requests
import json
from .config import omdb_key
import urllib
def get_information_list(movies):
    results = []
    for movie in movies:
        results.append(get_information(movie))
    return results

def get_information(movie):
    title = movie['title'].replace(' ', '+')
    data = requests.get('http://omdbapi.com/?t={}&apikey={}'.format(title, omdb_key))
    return json.loads(data.content)
