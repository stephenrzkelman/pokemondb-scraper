import requests
import re
from bs4 import BeautifulSoup

def get_pokemon_links():
    URL = "https://pokemondb.net/pokedex/national"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)

    pokemon_links = re.findall("<a class=\"ent-name\" href=\"\/pokedex\/[^\"]*\"", str(soup))
    pokemon_links = list(map(lambda href_link : "https://pokemondb.net"+href_link[26:-1], pokemon_links))
    # print(pokemon_links)

    return list(set(pokemon_links))

def get_pokemon_info(pokemon_links):
    for URL in pokemon_links:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        name = soup.find_all("h1")[0].text
        print(name)
        dex_data = soup.find_all(
            "h2", 
            # class_="grid-col span-md-6 span-lg-4",
            string="Pokédex data"
        )[0].parent
        type_tags = dex_data.find_all(
            "a",
            class_="type-icon"
        )
        types = [type_tag.text for type_tag in type_tags]
        print(types)
        return

pokemon_links = get_pokemon_links()
get_pokemon_info(pokemon_links)
