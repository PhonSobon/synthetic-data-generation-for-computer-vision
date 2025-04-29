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
#                 print(f"⛔ Excluding invalid font: {f} - {str(e)}")

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


def get_random_background(based_image_size: tuple, bg_dir: str, min_img_scale: float, max_img_scale: float) -> Image.Image:

    base_width = random.randint(int(
        based_image_size[0] * min_img_scale), int(based_image_size[0] * max_img_scale))
    base_height = random.randint(int(
        based_image_size[1] * min_img_scale), int(based_image_size[1] * max_img_scale))

    target_size = (base_width, base_height)

    random_choice = random.choice(["image", "color"])

    # Create background
    if random_choice == "image" and bg_dir:
        bg_images = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir)]
        if bg_images:
            bg = Image.open(random.choice(bg_images)).convert('RGB')
        else:
            bg = Image.new('RGB', target_size,
                           color=get_random_rgb())   # type: ignore
    else:
        bg = Image.new('RGB', target_size,
                       color=get_random_rgb())   # type: ignore

    bg = bg.resize(target_size)

    return bg


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
