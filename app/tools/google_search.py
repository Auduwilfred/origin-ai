import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

def google_search(query: str):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "num": 5
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        results = []

        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })

        return results

    except Exception as e:
        return [{"error": str(e)}]
