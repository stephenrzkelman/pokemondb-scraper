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
        # Get Name
        name = soup.find_all("h1")[0].text
        print(name)
        # Get Types
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
        # Get Base Stats
        dex_stats = soup.find(
            "h2",
            string="Base stats"
        ).parent
        stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        stats = {}
        for stat_name in stat_names:
            stat_section = dex_stats.find("th", string=stat_name).parent
            stat_value = stat_section.find("td", class_="cell-num").text
            stats[stat_name] = stat_value
        print(stats)
        return
        # stats = {}
        # for stat
        # print(stats)

        # return

pokemon_links = get_pokemon_links()
get_pokemon_info(pokemon_links)
