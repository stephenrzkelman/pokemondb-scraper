from bs4 import BeautifulSoup
import json
import requests
import os

def scrape_items():
    item_file = open('items.json', 'w')
    items_url = 'https://pokemondb.net/item/all#cat=hold'
    items_page = requests.get(items_url)
    items_html = BeautifulSoup(items_page.content, 'html.parser')
    item_boxes = items_html.find_all("tr")[1:]
    items = {}
    for item_box in item_boxes:
        item_infos = item_box.find_all("td")
        item_category = item_infos[1]["data-sort-value"]
        if item_category != "hold":
            continue
        item_name_box = item_infos[0]
        item_img_url = item_name_box.find("img")["src"]
        item_image_filename = scrape_image(item_img_url)
        item_name = item_name_box.find("a").text
        print(item_name)
        item_description = item_infos[2].text
        items[item_name] = {
            "image": item_image_filename,
            "description": item_description
        }

    json.dump(items, item_file)

    

def scrape_image(image_url):
    image = requests.get(image_url).content
    image_filename = image_url.split("/")[-1]
    with open(f"items/{image_filename}", "wb+") as image_file:
        image_file.write(image)
    return image_filename 

scrape_items()