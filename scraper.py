import requests
import re
from bs4 import BeautifulSoup

URL = "https://pokemondb.net/pokedex/national"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

pokemon_links = re.findall("<a class=\"ent-name\" href=\"\/pokedex\/[^\"]*\"", str(soup))
pokemon_links = list(map(lambda href_link : "https://pokemondb.net"+href_link[26:-1], pokemon_links))
# print(pokemon_links)

pokemon_links = list(set(pokemon_links))
