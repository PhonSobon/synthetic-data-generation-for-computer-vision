import numpy as np
from PIL import Image
import math
import dotenv
import os
import json
import random


dotenv.load_dotenv()

colors_raw = os.getenv("CANDIDATE_COLORS", default="{}")
CANDIDATE_COLORS = json.loads(colors_raw)
MIN_DISTANCE = int(os.getenv("MIN_DISTANCE", default=100))

def calculate_average_bg_color(img: Image.Image) -> tuple[int, int, int]:
    """Calculate the average color of the image"""
    img = img.convert("RGB")
    img_array = np.array(img)
    avg_color = img_array.mean(axis=(0, 1))
    return tuple(avg_color.astype(int))


def contrast_color(
    bg_color: tuple[int, int, int],
    candidates: dict = CANDIDATE_COLORS,
    min_distance: float = MIN_DISTANCE
) -> tuple[int, int, int]:
    
    """Calculate the contrast color based on the background color"""
    bg_r, bg_g, bg_b = bg_color
    # Compute distance to each candidate
    dist_list = []
    for name, (r, g, b) in candidates.items():
        dist = math.sqrt((bg_r - r)**2 + (bg_g - g)**2 + (bg_b - b)**2)
        dist_list.append((dist, (r, g, b)))

    # Filter for good contrast
    good = [rgb for dist, rgb in dist_list if dist >= min_distance]

    if good:
        return random.choice(good)
    else:
        # fallback: pick the single farthest color
        farthest = max(dist_list, key=lambda x: x[0])
        return farthest[1]


def get_contrast_color(image: Image.Image, x: int, y: int, w: int, h: int) -> tuple[int, int, int]:
    """Get color that contrasts with background region with safety checks"""
    
    # Ensure crop coordinates stay within image bounds
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(image.width, x + w)
    y1 = min(image.height, y + h)

    if x0 >= x1 or y0 >= y1:
        return (0, 0, 0)  # Fallback color

    region = image.crop((x0, y0, x1, y1))
    avg_color = calculate_average_bg_color(region)
    return contrast_color(avg_color)
