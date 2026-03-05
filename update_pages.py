import os
import re
import urllib.parse
from bs4 import BeautifulSoup

html_files = ["danang.html", "halong.html", "hoian.html", "ninhbinh.html", "phuquoc.html", "sapa.html"]

TIME_SLOTS = [
    "Sáng Ngày 1", "Chiều Ngày 1", "Sáng Ngày 2", "Chiều Ngày 2", 
    "Sáng Ngày 3", "Chiều Ngày 3", "Sáng Ngày 4"
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
        # some pages had overlay h4, some might have different structure.
        # But looking at danang.html, it's <div class="suggested-card-overlay"><h4>...</h4></div>
        title_tag = card.select_one("h4")
        if not title_tag: continue
        
        title = title_tag.text.strip()
        
        # generate pollinations URL. Using landscape ratio 500x350
        prompt = f"{title} destination beautiful cinematic landscape photography high quality detailed 4k"
        img_url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + "?width=500&height=350&nologo=true"
        
        # update image
        img_tag = card.select_one("img")
        if img_tag:
            img_tag["src"] = img_url
            
        # Add attributes for modal
        card["onclick"] = "openTourModal(this)"
        card["style"] = "cursor: pointer;"
        card["data-title"] = title
        card["data-img"] = img_url
        card["data-adv"] = f"🌟 SIÊU HOT: {title} đang là điểm đến được săn đón nhất!"
        card["data-desc"] = f"Bạn không thể bỏ lỡ {title} khi tới đây! Đây là một điểm sinh thái, check-in vô cùng hấp dẫn với vẻ đẹp độc đáo. Tham quan nơi đây, bạn sẽ bị cuốn hút bởi những khung cảnh lộng lẫy, không gian khoáng đạt và nền văn hoá đặc sắc. Vô vàn góc máy sống ảo \"không góc chết\" và những trải nghiệm thực tế khó quên đang chờ đón bạn."
        card["data-time"] = f"Lịch trình lý tưởng: Nhâm nhi vẻ đẹp vào {TIME_SLOTS[i % len(TIME_SLOTS)]}."
        
    # Check if CSS is already added
    head = soup.select_one("head")
    if head and not soup.select_one("link[href='assets/css/modal.css']"):
        css_tag = soup.new_tag("link", rel="stylesheet", href="assets/css/modal.css")
        head.append(css_tag)

    # Check if JS is already added
    body = soup.select_one("body")
    if body and not soup.select_one("script[src='assets/js/modal.js']"):
        script_tag = soup.new_tag("script", src="assets/js/modal.js")
        body.append(script_tag)
        
    # Save formatted
    with open(filepath, "w", encoding="utf-8") as f:
        # Avoid BeautifulSoup adding closing tags aggressively to wrong things, we write the string
        f.write(soup.prettify(formatter="html"))
