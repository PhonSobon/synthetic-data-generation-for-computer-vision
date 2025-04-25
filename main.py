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
    # Select multiple random words (adjust max_words as needed)
    max_words = 10  # Maximum number of words to place
    texts = random.choices(TEXT_WORDS, k=max_words)

    bg = get_random_background()
    base_width, base_height = bg.size
    draw = ImageDraw.Draw(bg)
    annotations = []

    for text in texts:
        # Get font and text dimensions
        font, text_width, text_height = get_dynamic_font(text, base_width, base_height)
        
        # Calculate available position space
        max_x = base_width - text_width
        max_y = base_height - text_height
        x = random.randint(0, max_x) if max_x > 0 else 0
        y = random.randint(0, max_y) if max_y > 0 else 0

        # Get color contrasting with the specific region
        region = bg.crop((x, y, x + text_width, y + text_height))
        text_color = contrast_color(calculate_average_color(region))
        
        # Draw text and store coordinates
        draw.text((x, y), text, fill=text_color, font=font)
        annotations.append((x, y, text_width, text_height))

    # Resize image
    bg = bg.resize(IMAGE_SIZE)
    scale_x = IMAGE_SIZE[0] / base_width
    scale_y = IMAGE_SIZE[1] / base_height

    yolo_annotations = []
    for (x, y, w, h) in annotations:
        # Scale coordinates
        scaled_x = x * scale_x
        scaled_y = y * scale_y
        scaled_w = w * scale_x
        scaled_h = h * scale_y

        # Clamp values to image boundaries
        scaled_x = max(0, min(scaled_x, IMAGE_SIZE[0] - 1))
        scaled_y = max(0, min(scaled_y, IMAGE_SIZE[1] - 1))
        scaled_w = max(1, min(scaled_w, IMAGE_SIZE[0] - scaled_x))
        scaled_h = max(1, min(scaled_h, IMAGE_SIZE[1] - scaled_y))

        # Convert to YOLO format
        x_center = (scaled_x + scaled_w / 2) / IMAGE_SIZE[0]
        y_center = (scaled_y + scaled_h / 2) / IMAGE_SIZE[1]
        width_norm = scaled_w / IMAGE_SIZE[0]
        height_norm = scaled_h / IMAGE_SIZE[1]

        yolo_annotations.append((0, x_center, y_center, width_norm, height_norm))

    return bg, yolo_annotations









if __name__ == "__main__":
    for i in range(NUM_IMAGES):
        img, bbox = create_text_image_with_bbox()
        
        # Apply post-processing artifacts
        img = apply_artifact(img)
        
        # Save image and label
        image_filename = f"img_{i:04d}.png"
        img.save(os.path.join(SAVE_DIR, image_filename))
        
        label_filename = f"img_{i:04d}.txt"
        with open(os.path.join(LABEL_DIR, label_filename), 'w') as f:
            for box in bbox:
                f.write(f"{box[0]} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f} {box[4]:.6f}\n")
            