import google.generativeai as genai
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

# Configure APIs and Email
GEMINI_API_KEY = "AIzaSyA_0BoXTxGHzM5Athd_cbac6b1Z6xZyJ9E"
SERPER_API_KEY = "5abce63108fa0916d4a9fd2b68635d875c0ddfa5"
EMAIL_ADDRESS = "muditagrawal9415369961@gmail.com"
EMAIL_PASSWORD = "cznhn meoq fkxn zpfo opy"  # App password for Gmail

def setup_gemini():
    """Initialize Gemini API configuration"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # List and find available models
        available_models = [m.name for m in genai.list_models()]
        print("Available models:", available_models)
        
        # Try to find the best available model
        if "models/gemini-2.5-pro" in available_models:
            model_name = "models/gemini-2.5-pro"
        elif "models/gemini-2.0-pro" in available_models:
            model_name = "models/gemini-2.0-pro"
        else:
            model_name = "gemini-pro"  # fallback to base model
            
        print(f"Using model: {model_name}")
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        print(f"Error setting up Gemini: {str(e)}")
        return None

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
    if not model:
        return "Error: Gemini model not properly initialized"
    
    try:
        prompt = create_blog_prompt(shops_data)
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return "Error: No content generated from the model"
            
        return response.text
    except Exception as e:
        error_msg = f"Error generating blog post: {str(e)}"
        print(error_msg)
        return f"Error generating blog post: {str(e)}\nPlease check your API key and try again."

def save_blog_post(content: str, filename: str = "blog_post.md"):
    """Save the generated blog post to a file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Blog post successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving blog post: {e}")

def send_email(content: str):
    """Send the blog post via email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = "Generated Blog Post: Clothes Shops in Satna"

        # Format the content for email
        formatted_content = content.replace('```markdown', '').replace('```', '')
        
        # Add body
        body = f"""
Hello!

Here's your generated blog post about clothes shops in Satna:

{formatted_content}

Best regards,
Blog Generator
        """
        msg.attach(MIMEText(body, 'plain'))

        print("Attempting to send email...")
        print(f"Using email address: {EMAIL_ADDRESS}")
        
        # Setup SMTP server with explicit error handling
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                print("Connected to SMTP server...")
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print("Logged in successfully...")
                server.send_message(msg)
                print("Message sent successfully!")
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Please check your email and app password.")
            print("Make sure you're using an App Password from Google Account settings.")
            return
        except smtplib.SMTPException as smtp_e:
            print(f"SMTP error occurred: {smtp_e}")
            return
        
        print("Blog post successfully sent to your email!")
    except Exception as e:
        print(f"Error sending email: {e}")
        print("Please check your email settings and try again.")

def main():
    try:
        # Initialize Gemini model
        model = setup_gemini()
        if not model:
            print("Failed to initialize Gemini model. Please check your API key and internet connection.")
            return

        # Fetch shops data
        print("Fetching shops data...")
        shops_data = get_shops_data()
        if not shops_data.get('organic'):
            print("No shop data found. Please check your Serper API key.")
            return

        # Generate blog post
        print("Generating blog post...")
        blog_post = generate_blog_post(model, shops_data)
        
        # Check if blog post was generated successfully
        if blog_post.startswith("Error"):
            print("Failed to generate blog post:")
            print(blog_post)
            return

        # Save blog post
        save_blog_post(blog_post)
        
        # Send email
        print("\nSending blog post via email...")
        send_email(blog_post)
        
        # Print preview
        print("\nBlog Post Preview:")
        print("=" * 50)
        preview = blog_post[:500] + "..." if len(blog_post) > 500 else blog_post
        print(preview)
        print("=" * 50)
        print("\nFull blog post has been saved to blog_post.md and sent to your email")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()