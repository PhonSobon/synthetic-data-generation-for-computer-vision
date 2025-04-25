import dotenv
from PIL import Image, ImageDraw, ImageFont
import os
import random
import numpy as np


dotenv.load_dotenv()

FONT_DIR = os.getenv("FONT_DIR", "fonts/")
FONT_SIZE = int(os.getenv("FONT_SIZE", 24))
MAX_FONT_SIZE = int(os.getenv("MAX_FONT_SIZE", 32))
MIN_FONT_SIZE = int(os.getenv("MIN_FONT_SIZE", 12))
IMAGE_SIZE = tuple(map(int, os.getenv("IMAGE_SIZE", "256,64").split(",")))
BACKGROUND_IMAGES_DIR = os.getenv("BACKGROUND_IMAGES_DIR", "background/")
MIN_PARAG_LENGTH = int(os.getenv("MIN_PARAGRAPH_LENGTH", 3))
MAX_PARAG_LENGTH = int(os.getenv("MAX_PARAGRAPH_LENGTH", 15))

def generate_random_paragraph(text_words):
    num_words = random.randint(MIN_PARAG_LENGTH, MAX_PARAG_LENGTH)
    return ' '.join(random.choices(text_words, k=num_words))


def get_random_rgb():
    return tuple(np.random.randint(0, 256, size=3))


def get_dynamic_font(text, max_width, max_height):
    """Find font size that ensures text fits within specified dimensions"""
    fonts = [os.path.join(FONT_DIR, f)
             for f in os.listdir(FONT_DIR) if f.endswith('.ttf')]
    chosen_font = random.choice(fonts)

    for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE-1, -1):
        font = ImageFont.truetype(chosen_font, size)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width * 0.9 and text_height <= max_height * 0.9:
            return font, text_width, text_height
    return ImageFont.truetype(chosen_font, MIN_FONT_SIZE), text_width, text_height


def get_random_background():

    # base_width = random.randint(int(IMAGE_SIZE[0] * 0.7), int(IMAGE_SIZE[0] * 1.3))
    # base_height = random.randint(int(IMAGE_SIZE[1] * 0.7), int(IMAGE_SIZE[1] * 1.3))

    target_size = IMAGE_SIZE

    random_choice = random.choice(["image", "color"])

    # Create background
    if random_choice == "image" and BACKGROUND_IMAGES_DIR:
        bg_images = [os.path.join(BACKGROUND_IMAGES_DIR, f) for f in os.listdir(BACKGROUND_IMAGES_DIR)]
        if bg_images:
            bg = Image.open(random.choice(bg_images)).convert('RGB')
            # bg = bg.resize((base_width, base_height))
            bg = bg.resize(target_size)
        else:
            bg = Image.new('RGB', target_size, color=get_random_rgb())  # type: ignore
    else:
        bg = Image.new('RGB', target_size, color=get_random_rgb())  # type: ignore

    bg = bg.resize(target_size)

    return bg
