import os
import random
from PIL import Image, ImageDraw
import dotenv


dotenv.load_dotenv()

TEXT_WORDS=[
    "ខ្ញុំ", "ស្រឡាញ់", "ភាសាខ្មែរ", "សូម", "ស្វាគមន៍", "ព្រះរាជាណាចក្រ",
    "សាលារៀន", "បច្ចេកវិទ្យា", "រាជធានី", "ភ្នំពេញ", "ជំនាញ", "បច្ចេកទេស"
]
SAVE_DIR = os.getenv("SAVE_DIR", "synthetic_images/")
LABEL_DIR = os.getenv("LABEL_DIR", "labels/")
IMAGE_SIZE = tuple(map(int, os.getenv("IMAGE_SIZE", "725,450").split(",")))
BACKGROUND_IMAGES_DIR = os.getenv("BACKGROUND_IMAGES_DIR", "background/")
NUM_IMAGES = int(os.getenv("NUM_IMAGES", 1))
PADDING = int(os.getenv("PADDING", 10))
LINE_SPACING = int(os.getenv("LINE_SPACING", 5))

# === HELPER FUNCTIONS ===
from helper.get_random import generate_random_paragraph, get_random_rgb, get_dynamic_font, get_random_background
from helper.get_color import contrast_color
from helper.image_processing import apply_artifact, apply_text_transform
from helper.text import wrap_text
from helper.calculation import calculate_transformed_bbox, calculate_average_color


def create_text_image_with_bbox():
    text = random.choice(TEXT_WORDS)

    bg = get_random_background()
    base_width, base_height = bg.size

    # Get dynamically sized font
    font, text_width, text_height = get_dynamic_font(text, base_width, base_height)
    
    # Random position with padding
    max_x = base_width - text_width
    max_y = base_height - text_height
    x = random.randint(0, max_x) if max_x > 0 else 0
    y = random.randint(0, max_y) if max_y > 0 else 0

    # Draw text
    draw = ImageDraw.Draw(bg)
    text_color = contrast_color(calculate_average_color(bg))
    draw.text((x, y), text, fill=text_color, font=font)

    # Apply random affine transformation
    # if random.random() < 0.5:
    #     scale_x = random.uniform(0.8, 1.2)
    #     scale_y = random.uniform(0.8, 1.2)
    #     shear_x = random.uniform(-0.2, 0.2)
    #     shear_y = random.uniform(-0.2, 0.2)
        
    #     bg = bg.transform(
    #         bg.size,
    #         Image.Transform.AFFINE,
    #         (scale_x, shear_x, -x * (scale_x - 1) - shear_x * y,
    #          shear_y, scale_y, -y * (scale_y - 1) - shear_y * x)
    #     )

    # Resize to target size
    bg = bg.resize(IMAGE_SIZE)
    
    # Calculate transformed coordinates
    scale_x = IMAGE_SIZE[0] / base_width
    scale_y = IMAGE_SIZE[1] / base_height
    x = x * scale_x
    y = y * scale_y
    text_width *= scale_x
    text_height *= scale_y

    # Ensure coordinates are within bounds
    x = max(0, min(x, IMAGE_SIZE[0] - 1))
    y = max(0, min(y, IMAGE_SIZE[1] - 1))
    text_width = max(1, min(text_width, IMAGE_SIZE[0] - x))
    text_height = max(1, min(text_height, IMAGE_SIZE[1] - y))

    # YOLO format
    x_center = (x + text_width / 2) / IMAGE_SIZE[0]
    y_center = (y + text_height / 2) / IMAGE_SIZE[1]
    w = text_width / IMAGE_SIZE[0]
    h = text_height / IMAGE_SIZE[1]

    return bg, (0, x_center, y_center, w, h)

# === GENERATION LOOP ===

for i in range(NUM_IMAGES):
    img, bbox = create_text_image_with_bbox()
    
    # Apply post-processing artifacts
    img = apply_artifact(img)
    
    # Save image and label
    image_filename = f"img_{i:04d}.png"
    img.save(os.path.join(SAVE_DIR, image_filename))
    
    label_filename = f"img_{i:04d}.txt"
    with open(os.path.join(LABEL_DIR, label_filename), 'w') as f:
        f.write(f"{bbox[0]} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f} {bbox[4]:.6f}\n")