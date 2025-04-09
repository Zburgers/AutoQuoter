"""
Image Creator Module
Generates quote images using PIL
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Tuple, Optional

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, 'backgrounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Default dimensions for quote images
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080

# Theme to background mapping (will fallback to random if theme not found)
THEME_BACKGROUNDS = {
    "motivation": ["mountain.jpg", "sunrise.jpg", "ocean.jpg"],
    "stoicism": ["stone.jpg", "ancient.jpg", "minimal.jpg"],
    "success": ["achievement.jpg", "summit.jpg", "victory.jpg"],
    "leadership": ["mountain.jpg", "path.jpg", "horizon.jpg"],
    "happiness": ["beach.jpg", "sunset.jpg", "flowers.jpg"],
}

# Default fonts to use
FONTS = {
    "primary": "opensans.ttf",
    "secondary": "playfair.ttf",
    "accent": "handwritten.ttf",
}


def create_quote_image(
    quote_text: str,
    author: str,
    theme: str = "motivation",
    output_path: str = None,
    add_watermark: bool = True
) -> str:
    """
    Create a quote image with the given text and author
    
    Args:
        quote_text: The quote text to render
        author: The author of the quote
        theme: Theme for background selection
        output_path: Where to save the image
        add_watermark: Whether to add AutoQuoter watermark
        
    Returns:
        Path to the generated image
    """
    # Make sure directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Get a background image based on theme
    background_path = get_background_for_theme(theme)
    
    # Create base image
    img = Image.open(background_path) if background_path else create_default_background()
    
    # Resize to standard dimensions
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    
    # Apply slight blur and darken for better text visibility
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    img = darken_image(img, factor=0.6)  # Darken by 40%
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    quote_font = get_font("primary", size=60)
    author_font = get_font("secondary", size=40)
    watermark_font = get_font("primary", size=24)
    
    # Calculate text dimensions and positions
    quote_lines = text_wrap(quote_text, quote_font, IMAGE_WIDTH - 200)
    quote_text_height = sum(draw.textbbox((0, 0), line, font=quote_font)[3] for line in quote_lines)
    
    # Position for the quote (centered)
    quote_y = (IMAGE_HEIGHT - quote_text_height - 120) // 2  # 120px space for author
    
    # Draw text with shadow for better visibility
    for line in quote_lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width = bbox[2]
        text_x = (IMAGE_WIDTH - text_width) // 2
        
        # Draw shadow/outline
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            draw.text((text_x + offset[0], quote_y + offset[1]), line, font=quote_font, fill=(0, 0, 0, 180))
        
        # Draw the actual text
        draw.text((text_x, quote_y), line, font=quote_font, fill=(255, 255, 255))
        quote_y += bbox[3] + 10  # Move down for next line + some spacing
    
    # Add author attribution
    author_text = f"— {author}"
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_width = author_bbox[2]
    author_x = (IMAGE_WIDTH - author_width) // 2
    author_y = quote_y + 40  # Below the quote text
    
    # Draw author with shadow
    for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
        draw.text((author_x + offset[0], author_y + offset[1]), author_text, font=author_font, fill=(0, 0, 0, 180))
    
    # Draw the actual author text
    draw.text((author_x, author_y), author_text, font=author_font, fill=(255, 255, 255))
    
    # Add watermark if needed
    if add_watermark:
        watermark_text = "AutoQuoter.com"
        watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
        watermark_width = watermark_bbox[2]
        watermark_x = (IMAGE_WIDTH - watermark_width) // 2
        watermark_y = IMAGE_HEIGHT - 60  # Near the bottom
        
        # Draw watermark with semi-transparency
        draw.text((watermark_x, watermark_y), watermark_text, font=watermark_font, fill=(255, 255, 255, 180))
    
    # Save the image
    img.save(output_path, "PNG")
    
    return output_path


def get_background_for_theme(theme: str) -> Optional[str]:
    """Get a background image path based on theme"""
    theme = theme.lower()
    
    # Get the list of background options for this theme
    background_options = THEME_BACKGROUNDS.get(theme, [])
    
    # If no specific backgrounds for theme, use random from all backgrounds
    if not background_options:
        background_files = os.listdir(BACKGROUNDS_DIR) if os.path.exists(BACKGROUNDS_DIR) else []
        if background_files:
            return os.path.join(BACKGROUNDS_DIR, random.choice(background_files))
        return None
    
    # Pick a random background from the theme options
    chosen_bg = random.choice(background_options)
    bg_path = os.path.join(BACKGROUNDS_DIR, chosen_bg)
    
    # Check if the file exists
    if os.path.exists(bg_path):
        return bg_path
    
    # Fallback to any available background
    background_files = os.listdir(BACKGROUNDS_DIR) if os.path.exists(BACKGROUNDS_DIR) else []
    if background_files:
        return os.path.join(BACKGROUNDS_DIR, random.choice(background_files))
    
    return None


def create_default_background() -> Image.Image:
    """Create a default gradient background if no image is available"""
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Create a simple gradient
    for y in range(IMAGE_HEIGHT):
        r = int(30 + (y / IMAGE_HEIGHT) * 40)
        g = int(30 + (y / IMAGE_HEIGHT) * 20)
        b = int(70 + (y / IMAGE_HEIGHT) * 30)
        draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
    
    return img


def get_font(font_key: str, size: int) -> ImageFont.FreeTypeFont:
    """Get a font with the specified size"""
    font_file = FONTS.get(font_key, "opensans.ttf")
    font_path = os.path.join(FONTS_DIR, font_file)
    
    # Check if the font exists
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size=size)
        except Exception:
            pass
    
    # Fallback to default font
    try:
        # Try to use a system font
        return ImageFont.truetype("arial.ttf", size=size)
    except Exception:
        # Last resort: use default font
        return ImageFont.load_default()


def text_wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
    """Wrap text to fit within max_width"""
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        # Try adding this word to the current line
        test_line = ' '.join(current_line + [word])
        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_line, font=font)
        text_width = bbox[2]
        
        if text_width <= max_width:
            # Word fits, add it to the current line
            current_line.append(word)
        else:
            # Word doesn't fit, start a new line
            if current_line:  # Only append if we have content
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def darken_image(img: Image.Image, factor: float = 0.7) -> Image.Image:
    """Darken an image to make text more readable"""
    darkened = img.copy()
    
    # Create a dark semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, int(255 * (1 - factor))))
    
    # Paste the overlay onto the image
    if darkened.mode == 'RGB':
        darkened = darkened.convert('RGBA')
    
    darkened = Image.alpha_composite(darkened.convert('RGBA'), overlay)
    darkened = darkened.convert('RGB')
    
    return darkened