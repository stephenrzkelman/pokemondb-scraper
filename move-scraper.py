from bs4 import BeautifulSoup
import json
import requests
import os

def scrape_moves():
    move_file = open('moves.json', 'w')
    moves_url = 'https://pokemondb.net/move/all'
    moves_page = requests.get(moves_url)
    moves_html = BeautifulSoup(moves_page.content, 'html.parser')
    move_boxes = moves_html.find_all("tr")[1:]
    print(len(move_boxes))
    moves = {}
    for move_box in move_boxes:
        move_name = move_box.find("td", class_="cell-name").find("a").text
        move_type = move_box.find("td", class_="cell-icon").find("a")
        move_type = move_type.text if move_type else '-'
        move_category = move_box.find("td", class_="text-center").find("img")
        move_category = move_category['title'] if move_category else '-'
        move_stats = move_box.find_all("td", class_="cell-num")
        move_power = move_stats[0].text
        move_accuracy = move_stats[1].text
        move_pp = move_stats[2].text
        # move_probability = move_stats[3].text
        moves[move_name] = {
            "type": move_type,
            "category": move_category,
            "power": move_power,
            "accuracy": move_accuracy,
            "pp": move_pp
        }
    # print(moves)
    json.dump(moves, move_file)


scrape_moves()
