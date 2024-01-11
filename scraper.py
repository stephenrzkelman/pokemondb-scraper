import requests
import re
from bs4 import BeautifulSoup
import json

def get_pokemon_links():
    URL = "https://pokemondb.net/pokedex/national"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)

    pokemon_links = re.findall("<a class=\"ent-name\" href=\"\/pokedex\/[^\"]*\"", str(soup))
    pokemon_links = list(map(lambda href_link : "https://pokemondb.net"+href_link[26:-1], pokemon_links))
    # print(pokemon_links)

    return list(set(pokemon_links))

def get_variant_name(pokemon_name, variant_name):
    if(variant_name == pokemon_name):
        return pokemon_name
    else:
        return pokemon_name + "-" + variant_name.split(" ")[0]

def get_pokemon_info(pokemon_links):
    pokemon_data = {}
    for URL in pokemon_links:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # Get Name
        name = soup.find_all("h1")[0].text
        print(name)
        # Get Variants
        variant_section = soup.find(
            "div",
            class_="sv-tabs-tab-list"
        )
        variants = list(map(
            lambda variant_header: variant_header.text,
            variant_section.find_all(
                "a",
                class_="sv-tabs-tab"
            )
        ))
        # print(variants)
        # Get Types
        dex_data = list(map(
            lambda dex_data_header: dex_data_header.parent,
            soup.find_all(
                "h2", 
                # class_="grid-col span-md-6 span-lg-4",
                string="Pokédex data"
            )
        ))
        type_tags = list(map(
            lambda dex_datum: dex_datum.find_all("a", class_="type-icon"),
            dex_data
        ))
        types = [
            [tag.text for tag in tags] for tags in type_tags
        ]
        variant_types = {variants[i]:types[i] for i in range(len(variants))}
        # print(types)
        # Get Base Stats
        dex_stats = list(map(
            lambda dex_stat_header: dex_stat_header.parent,
            soup.find_all(
                "h2",
                string="Base stats"
            )
        ))
        variant_dex_stats = {
            variants[i]:dex_stats[i] for i in range(len(variants))
        }
        stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        stats = {variant: {} for variant in variants}
        for variant in variants:
            for stat_name in stat_names:
                stat_section = variant_dex_stats[variant].find("th", string=stat_name).parent
                stat_value = stat_section.find("td", class_="cell-num").text
                stats[variant][stat_name] = stat_value
            # print(stats)
            pokemon_data[get_variant_name(name,variant)] = {
                "Base Stats": stats[variant],
                "Type": variant_types[variant]
            }
    return pokemon_data

def output_to_file(pokemon_data, filename):
    with open(filename, "w") as outfile:
        json.dump(pokemon_data, outfile)

pokemon_links = get_pokemon_links()
pokemon_data = get_pokemon_info(pokemon_links)
output_to_file(pokemon_data, "pokemon.json")

