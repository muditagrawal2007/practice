import google.generativeai as genai
import json
import requests
from typing import Dict, Any

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyA_0BoXTxGHzM5Athd_cbac6b1Z6xZyJ9E"
SERPER_API_KEY = "5abce63108fa0916d4a9fd2b68635d875c0ddfa5"

def setup_gemini():
    """Initialize Gemini API configuration"""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-pro')

def get_shops_data() -> Dict[str, Any]:
    """Fetch shops data from Serper API"""
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": "clothing shops near Satna, Madhya Pradesh",
        "type": "search"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Serper API: {e}")
        return {"organic": []}

def create_blog_prompt(shops_data: Dict[str, Any]) -> str:
    """Create a detailed prompt for the blog post"""
    shops_info = []
    for shop in shops_data.get('organic', []):
        shop_details = {
            'name': shop.get('title', ''),
            'description': shop.get('snippet', ''),
            'rating': shop.get('rating', 'N/A'),
            'position': shop.get('position', 'N/A')
        }
        shops_info.append(shop_details)
    
    shops_context = json.dumps(shops_info, indent=2)
    
    return f"""
    Write an engaging and informative blog post about clothing stores in Satna, Madhya Pradesh, with a special focus on V-Mart. 
    Use this data about local shops: {shops_context}

    The blog post should:
    1. Have an engaging title and introduction about Satna's fashion scene
    2. Highlight V-Mart's unique features, location, and offerings
    3. Discuss other notable stores in Satna as complementary shopping options
    4. Include practical shopping tips and best times to visit
    5. Add specific details about store locations and popular items
    6. Maintain a friendly, conversational tone
    7. Be around 800-1000 words with proper formatting
    8. Include a conclusion with shopping recommendations
    9. Use markdown formatting for headers and sections

    Focus on creating valuable content for shoppers while naturally promoting V-Mart.
    """

def generate_blog_post(model, shops_data: Dict[str, Any]) -> str:
    """Generate blog post using Gemini Pro"""
    try:
        prompt = create_blog_prompt(shops_data)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating blog post: {e}")
        return "Error generating blog post. Please try again."

def save_blog_post(content: str, filename: str = "blog_post.md"):
    """Save the generated blog post to a file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Blog post successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving blog post: {e}")

def main():
    # Initialize Gemini model
    model = setup_gemini()
    
    # Fetch shops data
    print("Fetching shops data...")
    shops_data = get_shops_data()
    
    # Generate blog post
    print("Generating blog post...")
    blog_post = generate_blog_post(model, shops_data)
    
    # Save blog post
    save_blog_post(blog_post)
    
    # Print preview
    print("\nBlog Post Preview:")
    print("=" * 50)
    print(blog_post[:500] + "...")
    print("=" * 50)
    print("\nFull blog post has been saved to blog_post.md")

if __name__ == "__main__":
    main()