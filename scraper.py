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

def get_variant_name_id(pokemon_name, variant_name, pokemon_id):
    if(variant_name == pokemon_name):
        return pokemon_name, pokemon_id
    else:
        variant_suffix = variant_name.split(" ")[0]
        pokemon_variant_name = pokemon_name + "-" + variant_suffix
        pokemon_variant_id = pokemon_id + "-" + variant_suffix
        return pokemon_variant_name, pokemon_variant_id


def get_pokemon_variants(pokemon_webpage):
    # get section with variants
    variant_section = pokemon_webpage.find(
        "div",
        class_="sv-tabs-tab-list"
    )
    # get actual names of variants
    variants = list(map(
        lambda variant_header: variant_header.text,
        variant_section.find_all(
            "a",
            class_="sv-tabs-tab"
        )
    ))
    # return list of variant names
    return variants


def get_pokemon_types(pokemon_webpage):
    # get all variant dex data sections
    dex_data = list(map(
        lambda dex_data_header: dex_data_header.parent,
        pokemon_webpage.find_all(
            "h2",
            string="Pokédex data"
        )
    ))
    # for each dex data section, extract the type headers
    type_tags = list(map(
        lambda dex_datum: dex_datum.find_all("a", class_="type-icon"),
        dex_data
    ))
    # extract the actual types
    types = [
        [tag.text for tag in tags] for tags in type_tags
    ]
    # return 2d list of type for each variant
    return types


def extract_stats(stat_data):
    stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    stats = {}
    for stat_name in stat_names:
        stat_bar = stat_data.find("th", string=stat_name).parent
        stat_value = stat_bar.find("td", class_="cell-num").text
        stats[stat_name]= stat_value
    return stats


def get_pokemon_base_stats(pokemon_webpage):
    # get base stat section
    dex_stats = list(map(
        lambda dex_stat_header: dex_stat_header.parent,
        pokemon_webpage.find_all(
            "h2",
            string="Base stats"
        )
    ))
    # extract actual stats
    stats = list(map(
        lambda stat_data: extract_stats(stat_data),
        dex_stats
    ))
    return stats


def get_pokemon_info(pokemon_links):
    pokemon_data = {}
    count = 0
    for URL in pokemon_links:
        # save index name for other web scraping
        pokemondb_name = URL.split("/")[-1]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # Get Name
        name = soup.find_all("h1")[0].text
        # Get Variants
        variants = get_pokemon_variants(soup)
        # Get Types
        types = get_pokemon_types(soup)
        # Get Base Stats
        stats = get_pokemon_base_stats(soup)
        # Combine Info
        for i in range(len(variants)):
            variant_name, variant_id = get_variant_name_id(name, variants[i], pokemondb_name)
            pokemon_data[variant_name] = {
                "ID": variant_id,
                "type": types[i],
                "stats": stats[i],
            }
        count += 1
        print(count)
    return pokemon_data

def output_to_file(pokemon_data, filename):
    with open(filename, "w") as outfile:
        json.dump(pokemon_data, outfile)

pokemon_links = get_pokemon_links()
pokemon_data = get_pokemon_info(pokemon_links)
output_to_file(pokemon_data, "pokemon.json")

