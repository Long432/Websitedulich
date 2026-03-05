import os
import re
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

def get_wiki_image(keyword):
    try:
        url = f"https://vi.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&generator=search&gsrsearch={urllib.parse.quote(keyword)}&gsrlimit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            pages = res.get("query", {}).get("pages", {})
            for page_id in pages:
                if "original" in pages[page_id]:
                    return pages[page_id]["original"]["source"]
    except Exception as e:
        pass
    return None

html_files = ["danang.html", "halong.html", "hoian.html", "ninhbinh.html", "phuquoc.html", "sapa.html"]

PICS = [
    "https://images.unsplash.com/photo-1596404754792-7f5ccbb606f2?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1628126235206-5260b9ea6441?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1579201990499-56fb0ea6add5?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1583417316335-9f5b2daefc0b?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1563214820-22c97aee410b?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1558223608-f463cc1ba0ca?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1559480112-9c1c5a9478f6?q=80&w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1595856417740-9a4f475da4a0?q=80&w=500&auto=format&fit=crop",
]

for filename in html_files:
    filepath = os.path.join("d:\\Websitedulich", filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    cards = soup.select(".suggested-card")
    for i, card in enumerate(cards):
        title_tag = card.select_one("h4")
        if not title_tag: continue
        
        title = title_tag.text.strip()
        
        wiki_img = get_wiki_image(title)
        if wiki_img:
            img_url = wiki_img
        else:
            # try with shorter name if " - " exists
            short_name = title.split("-")[0].strip()
            wiki_img2 = get_wiki_image(short_name)
            if wiki_img2:
                img_url = wiki_img2
            else:
                img_url = PICS[(i + hash(filename)) % len(PICS)]
        
        img_tag = card.select_one("img")
        if img_tag:
            img_tag["src"] = img_url
            
        card["data-img"] = img_url
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(soup.prettify(formatter="html"))
        
print("Updated successfully!")
