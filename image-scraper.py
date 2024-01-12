import json
import requests

pokemon_file = open('pokemon.json')
pokemon = json.load(pokemon_file)
count = 0
for mon in pokemon.keys():
    print(mon)
    count += 1
    id = pokemon[mon]["ID"]
    gen8_url = f"https://img.pokemondb.net/sprites/sword-shield/normal/{id}.png"
    gen9_url = f"https://img.pokemondb.net/sprites/scarlet-violet/normal/{id}.png"
    gen8_response = requests.get(gen8_url)        
    gen9_response = requests.get(gen9_url)
    if gen8_response.status_code == 200:
        with open(f"images/{id}.png", "wb+") as image_file:
            image_file.write(gen8_response.content)
    elif gen9_response.status_code:
        with open(f"images/{id}.png", "wb+") as image_file:
            image_file.write(gen9_response.content)
    else:
        print(f"{mon} not available in gen 8 or gen 9")
    if count >= 5:
        break