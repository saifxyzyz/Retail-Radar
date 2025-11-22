from serpapi import GoogleSearch
from toon_python import encode
import json

def track_price(product):
    params = {
        "engine": "google_shopping",
        "q": product,
        "location": "Hyderabad, Telangana, India",
        "sort_by": "1",
        "num": "10",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "in",
        "api_key": "82f43ef55075a1e29270f6d8bfa52e708bf4a4eb3e9dada2dc9144552d050443"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    json_output = json.dumps(results, ensure_ascii=False)
    return json_output

