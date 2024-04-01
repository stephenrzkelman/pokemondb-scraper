import requests
from bs4 import BeautifulSoup

def scrape_moves(pokemon_page):
    move_section = pokemon_page.find(
        "div",
        class_ = "tabset-moves-game"
    )
    move_chunks = move_section.find_all(
        "td",
        class_ = "cell-name"
    )
    moves = list(map(
        lambda move_chunk: move_chunk.find(
            "a",
            class_ = "ent-name"
        ).text,
        move_chunks
    ))
    distinct_moves = list(set(moves))
    return distinct_moves


page = requests.get("https://pokemondb.net/pokedex/darmanitan")
soup = BeautifulSoup(page.content, "html.parser")
print(scrape_moves(soup))