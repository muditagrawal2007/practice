def validate_api_key(api_key):
    """Validate if the API key is in the correct format"""
    if not api_key or not isinstance(api_key, str) or len(api_key) != 40:
        raise ValueError("Invalid API key format. Please provide a valid Serper API key.")
    return True

def fetch_clothing_shops(api_key, location="Satna, Madhya Pradesh"):
    """Fetch clothing shops data from Serper API"""
    import requests
    
    validate_api_key(api_key)
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": f"clothing shops near {location}",
        "type": "search"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

def parse_shops_data(data):
    """Parse raw API response data into structured shop information"""
    shops = []
    for item in data.get('organic', []):
        shop_info = {
            'name': item.get('title'),
            'description': item.get('snippet'),
            'link': item.get('link'),
            'address': item.get('places', {}).get('address', 'N/A'),
            'rating': item.get('rating', 'N/A'),
            'reviews': item.get('places', {}).get('reviews', 'N/A')
        }
        shops.append(shop_info)
    return shops

def format_shops_output(shops):
    output = []
    for shop in shops:
        output.append(f"Name: {shop['name']}\nDescription: {shop['description']}\nLink: {shop['link']}\nAddress: {shop['address']}\nRating: {shop['rating']}\nReviews: {shop['reviews']}\n")
    return "\n".join(output)