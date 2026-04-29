import requests

def web_search(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    res = requests.get(url).json()

    return res.get("AbstractText", "No results found")
