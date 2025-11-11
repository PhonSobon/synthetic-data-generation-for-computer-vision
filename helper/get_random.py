from PIL import Image, ImageFont
from PIL.ImageFont import FreeTypeFont
import os
import random

_VALID_FONTS_CACHE: list[str] = []

def get_random_rgb() -> tuple[int, int, int]:
    """Generate a random RGB color"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_random_font(font_dir: str) -> str:
    """Get a random font from the specified directory"""
    fonts = [os.path.join(font_dir, f) for f in os.listdir(font_dir) if f.endswith('.ttf')]
    chosen_font = random.choice(fonts)
    return chosen_font


# def get_random_font(font_dir: str, font_size: int = 40) -> str:
#     """Get a random validated font with built-in checks"""
#     global _VALID_FONTS_CACHE

#     # Load and cache fonts on first call
#     if not _VALID_FONTS_CACHE:
#         test_chars = "កខគឃង"  # Test Latin + Khmer characters
#         font_files = [f for f in os.listdir(
#             font_dir) if f.lower().endswith(('.ttf', '.otf'))]

#         for f in font_files:
#             font_path = os.path.join(font_dir, f)
#             try:
#                 font = ImageFont.truetype(font_path, font_size)
#                 # Validate font can render required characters
#                 font.getbbox(test_chars)
#                 _VALID_FONTS_CACHE.append(font_path)
#             except Exception as e:
#                 print(f"Excluding invalid font: {f} - {str(e)}")

#         if not _VALID_FONTS_CACHE:
#             raise RuntimeError(f"No valid fonts found in {font_dir}")

#     # Get random validated font
#     chosen_path = random.choice(_VALID_FONTS_CACHE)

#     try:
#         return chosen_path
#     except Exception as e:
#         # Remove bad font from cache and retry
#         _VALID_FONTS_CACHE.remove(chosen_path)
#         print(
#             f"Removed invalid font from cache: {os.path.basename(chosen_path)}")
#         return get_random_font(font_dir, font_size)


def get_random_background(size, bg_dir, min_scale, max_scale):
    # If bg_dir is a dictionary or color, create solid color background
    if isinstance(bg_dir, dict) and "white" in bg_dir:
        return Image.new('RGB', size, color=bg_dir["white"])
    
    # If it's a path but directory doesn't exist, use white
    if not os.path.exists(bg_dir):
        return Image.new('RGB', size, color='white')
    
    # Original logic for image backgrounds
    try:
        bg_images = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir)]
        bg_images = [f for f in bg_images if os.path.isfile(f)]
        
        if not bg_images:
            return Image.new('RGB', size, color='white')
            
        bg_path = random.choice(bg_images)
        bg = Image.open(bg_path)
        # ... rest of original scaling logic
    except OSError:
        return Image.new('RGB', size, color='white')


def get_random_img_padding(min_img_padding: int, max_img_padding: int) -> tuple[int, int]:
    x_padding = random.randint(min_img_padding, max_img_padding)
    y_padding = random.randint(min_img_padding, max_img_padding)
    return x_padding, y_padding


def get_random_line_spacing(min_line_spacing: int, max_line_spacing: int) -> int:
    return random.randint(min_line_spacing, max_line_spacing)


def get_random_font_size(min_font_size: int, max_font_size: int) -> int:
    return random.randint(min_font_size, max_font_size)


def get_random_word_padding(min_word_padding: int, max_word_padding: int) -> int:
    return random.randint(min_word_padding, max_word_padding)
