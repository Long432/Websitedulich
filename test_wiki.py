import urllib.request
import urllib.parse
import json

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
        print("Error:", e)
    return None

print("Cầu Vàng:", get_wiki_image("Cầu Vàng"))
print("Bà Nà Hills:", get_wiki_image("Bà Nà Hills"))
print("Biển Mỹ Khê:", get_wiki_image("Biển Mỹ Khê"))
print("Chợ Cồn:", get_wiki_image("Chợ Cồn Đà Nẵng"))
print("Cầu Rồng:", get_wiki_image("Cầu Rồng"))
