"""
AutoQuoter - Main Flask Application
Handles API routes for the quote generator
"""
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
import os
import time
import json
from quote_fetcher import get_quote_by_theme
from image_creator import create_quote_image
from utils import cleanup_old_files

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__, 
           static_folder=os.path.join(BASE_DIR, 'static'),
           template_folder=os.path.join(BASE_DIR, 'templates'))
CORS(app)  # Enable CORS for all routes

# Configuration
GENERATED_DIR = os.path.join(BASE_DIR, 'static', 'generated')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
os.makedirs(GENERATED_DIR, exist_ok=True)

# User tracking (temporary in-memory storage - would use a database in production)
user_quotas = {}  # {ip_address: {count: int, last_reset: timestamp}}
FREE_TIER_LIMIT = 5
QUOTA_RESET_HOURS = 24


@app.route('/')
def index():
    """Serve the frontend application"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend files"""
    return send_from_directory(FRONTEND_DIR, path)


@app.route('/api/generate', methods=['POST'])
def generate_quote():
    """Generate a quote image based on theme and optional custom text"""
    try:
        # Get client IP for tracking quota
        client_ip = request.remote_addr
        
        # Check if user has exceeded quota
        if not check_user_quota(client_ip):
            return jsonify({"error": "Daily quota exceeded. Upgrade to premium for unlimited quotes."}), 429
        
        # Parse request data
        data = request.json
        theme = data.get('theme', 'motivation')
        custom_quote = data.get('customQuote')
        remove_watermark = data.get('removeWatermark', False)
        
        # Premium feature check (would be tied to actual auth in production)
        if remove_watermark:
            # For now, no one is premium
            remove_watermark = False
        
        # Get quote text (either custom or from API)
        if custom_quote:
            quote_text = custom_quote
            author = "Custom Quote"
        else:
            quote_data = get_quote_by_theme(theme)
            quote_text = quote_data['text']
            author = quote_data['author'] or "Unknown"
        
        # Generate a unique filename
        timestamp = int(time.time())
        filename = f"quote_{timestamp}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        
        # Create the quote image
        create_quote_image(
            quote_text=quote_text,
            author=author,
            theme=theme,
            output_path=output_path,
            add_watermark=not remove_watermark
        )
        
        # Increment user quota
        increment_user_quota(client_ip)
        
        # Cleanup old files
        cleanup_old_files(GENERATED_DIR, max_age_hours=24, max_files=100)
        
        # Return the generated image
        return send_file(output_path, mimetype='image/png')
    
    except Exception as e:
        app.logger.error(f"Error generating quote: {str(e)}")
        return jsonify({"error": "Failed to generate quote image", "message": str(e)}), 500


def check_user_quota(ip_address):
    """Check if user has remaining quota"""
    current_time = time.time()
    
    # If user not in tracking, add them
    if ip_address not in user_quotas:
        user_quotas[ip_address] = {"count": 0, "last_reset": current_time}
        return True
    
    # Check if we should reset quota (24 hours passed)
    user_data = user_quotas[ip_address]
    hours_passed = (current_time - user_data["last_reset"]) / 3600
    
    if hours_passed >= QUOTA_RESET_HOURS:
        user_quotas[ip_address] = {"count": 0, "last_reset": current_time}
        return True
    
    # Check if user still has quota
    return user_data["count"] < FREE_TIER_LIMIT


def increment_user_quota(ip_address):
    """Increment user's quote count"""
    if ip_address in user_quotas:
        user_quotas[ip_address]["count"] += 1


@app.route('/api/quota', methods=['GET'])
def get_user_quota():
    """Get user's remaining quota"""
    client_ip = request.remote_addr
    
    if client_ip not in user_quotas:
        remaining = FREE_TIER_LIMIT
    else:
        user_data = user_quotas[client_ip]
        
        # Check if we should reset
        current_time = time.time()
        hours_passed = (current_time - user_data["last_reset"]) / 3600
        
        if hours_passed >= QUOTA_RESET_HOURS:
            remaining = FREE_TIER_LIMIT
        else:
            remaining = FREE_TIER_LIMIT - user_data["count"]
    
    return jsonify({
        "remaining": remaining,
        "limit": FREE_TIER_LIMIT,
        "isPremium": False  # Would be tied to auth in production
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)