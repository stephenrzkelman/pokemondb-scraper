import json
import requests
import os

def scrape_images():
    pokemon_file = open('pokemon.json')
    pokemon = json.load(pokemon_file)
    for mon in pokemon.keys():
        print(mon)
        id = mon.lower()
        mon_image_file = f"images/{id}.png"
        if os.path.exists(mon_image_file):
            # skip if we already have the image
            continue
        gen8_url = f"https://img.pokemondb.net/sprites/sword-shield/normal/{id}.png"
        gen9_url = f"https://img.pokemondb.net/sprites/scarlet-violet/normal/{id}.png"
        gen6_url = f"https://img.pokemondb.net/sprites/x-y/normal/{id}.png"
        gen8_response = requests.get(gen8_url)        
        gen9_response = requests.get(gen9_url)
        gen6_response = requests.get(gen6_url)
        if gen8_response.status_code == 200:
            with open(mon_image_file, "wb+") as image_file:
                image_file.write(gen8_response.content)
        elif gen9_response.status_code == 200:
            with open(mon_image_file, "wb+") as image_file:
                image_file.write(gen9_response.content)
        elif gen6_response.status_code == 200:
            with open(mon_image_file, "wb+") as image_file:
                image_file.write(gen6_response.content)
        else:
            print(f"{mon} not available in gen 8 or gen 9")


scrape_images()