import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def fetch_clothing_shops(api_key, location="Satna, Madhya Pradesh"):
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": f"clothing shops near {location}",
        "type": "search"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print("\nAPI Response Structure:")
        print("======================")
        print(json.dumps(data, indent=2))
        print("\n======================\n")
        
        shops = []
        for item in data.get('organic', []):
            shop_info = {
                "name": item.get('title'),
                "description": item.get('snippet'),
                "link": item.get('link'),
                "address": item.get('places', {}).get('address', 'N/A'),
                "rating": item.get('rating', 'N/A')
            }
            shops.append(shop_info)
        
        return shops
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    api_key = "5abce63108fa0916d4a9fd2b68635d875c0ddfa5"
    shops = fetch_clothing_shops(api_key)
    
    for shop in shops:
        print(f"Name: {shop['name']}")
        print(f"Description: {shop['description']}")
        print(f"Link: {shop['link']}")
        print(f"Address: {shop['address']}")
        print(f"Rating: {shop['rating']}")
        print("-" * 40)