import os
from bs4 import BeautifulSoup

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
    
    # Process suggested cards
    cards = soup.select(".suggested-card")
    for i, card in enumerate(cards):
        img_url = PICS[(i + hash(filename)) % len(PICS)]
        
        # update image
        img_tag = card.select_one("img")
        if img_tag:
            img_tag["src"] = img_url
            
        card["data-img"] = img_url
        
    # Save formatted
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(soup.prettify(formatter="html"))
