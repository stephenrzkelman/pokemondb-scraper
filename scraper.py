import requests
import re
from bs4 import BeautifulSoup

URL = "https://pokemondb.net/pokedex/national"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# print(soup)
print(type(soup))

pokemon_links = re.findall("href=\"\/pokedex\/[^\"]*\"", str(soup))
pokemon_links = list(map(lambda href_link : "pokemondb.net"+href_link[6:-1], pokemon_links))
print(pokemon_links)