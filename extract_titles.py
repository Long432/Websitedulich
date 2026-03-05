import os
import json
from bs4 import BeautifulSoup

html_files = ["danang.html", "halong.html", "hoian.html", "ninhbinh.html", "phuquoc.html", "sapa.html"]
locations = {}

for filename in html_files:
    filepath = os.path.join("d:\\Websitedulich", filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".suggested-card")
    for card in cards:
        title_tag = card.select_one("h4")
        if title_tag:
            title = title_tag.text.strip()
            locations[title] = filename

with open(r"d:\Websitedulich\titles.json", "w", encoding="utf-8") as f:
    json.dump(locations, f, ensure_ascii=False, indent=2)
