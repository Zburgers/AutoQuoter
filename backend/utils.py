"""
Utility Functions for AutoQuoter
"""
import os
import time
import glob
from typing import List

def cleanup_old_files(directory: str, max_age_hours: int = 24, max_files: int = 100) -> None:
    """
    Clean up old generated files to prevent storage issues
    
    Args:
        directory: Directory to clean up
        max_age_hours: Maximum age of files to keep (in hours)
        max_files: Maximum number of files to keep
    """
    if not os.path.exists(directory):
        return
    
    # Get all files in the directory
    files = glob.glob(os.path.join(directory, "*.*"))
    
    # Sort files by modification time (oldest first)
    files.sort(key=lambda x: os.path.getmtime(x))
    
    # Remove old files based on count
    if len(files) > max_files:
        files_to_remove = files[:-max_files]  # Keep the newest 'max_files' files
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
        
        # After removing based on count, return early
        return
    
    # Remove files older than max_age_hours
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in files:
        file_modified_time = os.path.getmtime(file_path)
        if current_time - file_modified_time > max_age_seconds:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")


def ensure_directories_exist() -> None:
    """Ensure all required directories exist"""
    required_dirs = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'generated'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'backgrounds'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts'),
    ]
    
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)


def get_file_type(file_path: str) -> str:
    """Get the type of a file based on extension"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'image'
    elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
        return 'video'
    elif ext in ['.ttf', '.otf']:
        return 'font'
    else:
        return 'unknown'


def get_available_backgrounds() -> List[str]:
    """Get a list of available background images"""
    backgrounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'backgrounds')
    
    if not os.path.exists(backgrounds_dir):
        return []
    
    # Get image files
    image_extensions = ['.jpg', '.jpeg', '.png']
    backgrounds = []
    
    for ext in image_extensions:
        backgrounds.extend(glob.glob(os.path.join(backgrounds_dir, f"*{ext}")))
    
    # Return just the filenames, not full paths
    return [os.path.basename(bg) for bg in backgrounds]


def get_available_fonts() -> List[str]:
    """Get a list of available fonts"""
    fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')
    
    if not os.path.exists(fonts_dir):
        return []
    
    # Get font files
    font_extensions = ['.ttf', '.otf']
    fonts = []
    
    for ext in font_extensions:
        fonts.extend(glob.glob(os.path.join(fonts_dir, f"*{ext}")))
    
    # Return just the filenames, not full paths
    return [os.path.basename(font) for font in fonts]