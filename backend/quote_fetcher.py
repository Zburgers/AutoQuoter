"""
Quote Fetcher Module
Fetches quotes from various APIs based on themes
"""
import requests
import random
import json
import os
from typing import Dict, List, Any

# API endpoints
APIS = {
    "zenquotes": "https://zenquotes.io/api/random",
    "type_fit": "https://type.fit/api/quotes",
    "stoic": "https://stoic-api.herokuapp.com/api/quote",
}

# Cache quotes to reduce API calls
QUOTE_CACHE = {}
THEME_KEYWORDS = {
    "motivation": ["motivation", "inspire", "dream", "success", "goal", "action"],
    "stoicism": ["stoic", "virtue", "calm", "acceptance", "adversity", "obstacle"],
    "success": ["success", "achievement", "victory", "winning", "accomplish", "excel"],
    "leadership": ["leader", "guide", "vision", "influence", "inspire", "direction"],
    "happiness": ["happy", "joy", "content", "smile", "peace", "pleasure", "delight"],
}


def get_quote_by_theme(theme: str) -> Dict[str, str]:
    """
    Fetch a quote based on the requested theme
    Returns a dict with 'text' and 'author' keys
    """
    # Prioritize ZenQuotes API as the primary source
    quote = get_zen_quote()
    
    # If ZenQuotes fails or we need a specific theme
    if not quote or (theme.lower() == "stoicism"):
        # For stoicism theme, use dedicated stoic API
        if theme.lower() == "stoicism":
            return get_stoic_quote()
            
        # Try to fetch from Type.fit which has a large collection
        quotes = get_typeit_quotes()
        
        # Filter quotes by theme
        theme_keywords = THEME_KEYWORDS.get(theme.lower(), ["inspire", "motivation"])
        matching_quotes = []
        
        for q in quotes:
            quote_text = q.get("text", "").lower()
            for keyword in theme_keywords:
                if keyword in quote_text:
                    matching_quotes.append(q)
                    break
        
        # If we have matching quotes, return a random one
        if matching_quotes:
            chosen_quote = random.choice(matching_quotes)
            return {
                "text": chosen_quote.get("text", ""),
                "author": chosen_quote.get("author", "Unknown")
            }
    
    # Return ZenQuotes result or fallback
    return quote


def get_zen_quote() -> Dict[str, str]:
    """Fetch a quote from ZenQuotes API"""
    try:
        response = requests.get(APIS["zenquotes"])
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote = data[0]
                return {
                    "text": quote.get("q", ""),
                    "author": quote.get("a", "Unknown")
                }
    except Exception as e:
        print(f"Error fetching from ZenQuotes: {e}")
    
    # Return None to indicate failure
    return None


def get_stoic_quote() -> Dict[str, str]:
    """Fetch a stoic quote"""
    try:
        response = requests.get(APIS["stoic"])
        if response.status_code == 200:
            data = response.json()
            return {
                "text": data.get("quote", ""),
                "author": data.get("author", "Unknown")
            }
    except Exception as e:
        print(f"Error fetching from Stoic API: {e}")
    
    # Fallback to a stoic-themed default quote
    return {
        "text": "The obstacle is the way.",
        "author": "Marcus Aurelius"
    }


def get_typeit_quotes() -> List[Dict[str, Any]]:
    """Fetch quotes from Type.fit API with caching"""
    global QUOTE_CACHE
    
    # Check cache first
    if "type_fit" in QUOTE_CACHE:
        return QUOTE_CACHE["type_fit"]
    
    try:
        response = requests.get(APIS["type_fit"])
        if response.status_code == 200:
            quotes = response.json()
            QUOTE_CACHE["type_fit"] = quotes
            return quotes
    except Exception as e:
        print(f"Error fetching from Type.fit: {e}")
    
    # Return a small default list if API fails
    return [
        {"text": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
        {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
        {"text": "Quality is not an act, it is a habit.", "author": "Aristotle"},
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"}
    ]


def get_default_quote() -> Dict[str, str]:
    """Return a default quote if all APIs fail"""
    default_quotes = [
        {"text": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
        {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
        {"text": "Quality is not an act, it is a habit.", "author": "Aristotle"},
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"}
    ]
    return random.choice(default_quotes)