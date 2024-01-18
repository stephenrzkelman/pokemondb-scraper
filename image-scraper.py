import json
import requests
import os

def scrape_images():
    record_file = open('not-found.txt', 'w', encoding="utf-8")
    pokemon_file = open('pokemon.json')
    pokemon = json.load(pokemon_file)
    for mon in pokemon.keys():
        print(mon)
        id = pokemon[mon]["ID"]
        mon_image_file = f"images/{id}.png"
        if os.path.exists(mon_image_file):
            # skip if we already have the image
            continue
        generation_names = ["black-white", "x-y", "sun-moon", "sword-shield", "scarlet-violet"]
        def generation_url(generation_name):
            return f"https://img.pokemondb.net/sprites/{generation_name}/normal/{id}.png"
        generation_responses = list(map(
            lambda gen: requests.get(generation_url(gen)),
            generation_names
        ))
        for response in generation_responses:
            if response.status_code == 200:
                with open(mon_image_file, "wb+") as image_file:
                    image_file.write(response.content)
                continue
        # print(f"{mon} ({id}) sprite not found in gen 5-9 main games")
        record_file.write(f"{mon} ({id})\n")


scrape_images()