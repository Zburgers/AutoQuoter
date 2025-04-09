"""
Background Generator
Creates sample background images for AutoQuoter
"""
from PIL import Image, ImageDraw
import os
import math

# Ensure the backgrounds directory exists
backgrounds_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'backgrounds')
os.makedirs(backgrounds_dir, exist_ok=True)

# Create a variety of gradient backgrounds
def create_gradient(filename, dimensions, color1, color2, gradient_type='linear'):
    width, height = dimensions
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    if gradient_type == 'linear':
        # Linear gradient from top to bottom
        for y in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    elif gradient_type == 'radial':
        # Radial gradient from center
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        # For radial gradients, use a more efficient approach
        # by drawing rectangles of decreasing size
        for radius in range(int(max_dist), 0, -1):
            ratio = radius / max_dist
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            
            # Draw a filled ellipse with this color
            bbox = (center_x - radius, center_y - radius, 
                   center_x + radius, center_y + radius)
            draw.ellipse(bbox, fill=(r, g, b))
    
    img.save(os.path.join(backgrounds_dir, filename))
    print(f"Created {filename}")

# Define gradients to create
gradients = [
    # Theme: Motivation
    ('mountain.jpg', (1080, 1080), (66, 103, 178), (24, 59, 107), 'linear'),
    ('sunrise.jpg', (1080, 1080), (255, 153, 102), (204, 51, 51), 'radial'),
    ('ocean.jpg', (1080, 1080), (0, 153, 204), (0, 51, 102), 'linear'),
    
    # Theme: Stoicism
    ('stone.jpg', (1080, 1080), (102, 102, 102), (51, 51, 51), 'linear'),
    ('ancient.jpg', (1080, 1080), (153, 132, 107), (77, 66, 54), 'linear'),
    ('minimal.jpg', (1080, 1080), (230, 230, 230), (180, 180, 180), 'radial'),
    
    # Theme: Success
    ('achievement.jpg', (1080, 1080), (255, 215, 0), (204, 85, 0), 'radial'),
    ('summit.jpg', (1080, 1080), (102, 153, 204), (51, 51, 153), 'linear'),
    ('victory.jpg', (1080, 1080), (153, 204, 50), (51, 153, 102), 'linear'),
    
    # Theme: Leadership
    ('path.jpg', (1080, 1080), (102, 51, 153), (51, 0, 102), 'linear'),
    ('horizon.jpg', (1080, 1080), (51, 153, 255), (0, 102, 204), 'linear'),
    
    # Theme: Happiness
    ('beach.jpg', (1080, 1080), (255, 204, 102), (255, 153, 51), 'linear'),
    ('sunset.jpg', (1080, 1080), (255, 102, 102), (153, 51, 51), 'radial'),
    ('flowers.jpg', (1080, 1080), (255, 153, 204), (204, 51, 153), 'linear'),
]

# Create all gradients
for gradient in gradients:
    create_gradient(*gradient)

print(f"Created {len(gradients)} background images in {backgrounds_dir}")