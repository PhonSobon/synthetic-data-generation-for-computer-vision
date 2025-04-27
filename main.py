import os
import random
from PIL import ImageDraw
import dotenv


dotenv.load_dotenv()

with open("oscar_kh_1_cleaned.txt", "r", encoding='utf-8') as f:
    TEXT_WORDS = f.read().splitlines()
    if not TEXT_WORDS:
        print("No words found in the text file.")
        exit()

SAVE_DIR = os.getenv("SAVE_DIR", "synthetic_images/")
LABEL_DIR = os.getenv("LABEL_DIR", "labels/")
IMAGE_SIZE = tuple(map(int, os.getenv("IMAGE_SIZE", "725,450").split(",")))
BACKGROUND_IMAGES_DIR = os.getenv("BACKGROUND_IMAGES_DIR", "background/")
NUM_IMAGES = int(os.getenv("NUM_IMAGES", 1))
WORD_PADDING = int(os.getenv("WORD_PADDING", 10))
LINE_SPACING = int(os.getenv("LINE_SPACING", 5))
MAX_PARAG_LENGTH = int(os.getenv("MAX_PARAG_LENGTH", 15))
IMG_PADDING = int(os.getenv("IMG_PADDING", 30))

# === HELPER FUNCTIONS ===
from helper.get_random import get_dynamic_font, get_random_background, get_random_font
from helper.get_color import contrast_color
from helper.image_processing import apply_artifact, adjust_brightness_contrast_alpha_beta
from helper.calculation import calculate_average_color


def create_text_image_with_bbox():
    
    bg, texts = prepare_base_image_and_texts(MAX_PARAG_LENGTH)
    base_width, base_height = bg.size
    
    # Adjust available space for padding
    content_width = base_width - 2 * IMG_PADDING
    content_height = base_height - 2 * IMG_PADDING
    
    drawn_image, annotations = draw_texts_on_image(
        bg, texts, content_width, content_height, IMG_PADDING, LINE_SPACING
    )

    resized_image = drawn_image.resize(IMAGE_SIZE)
    
    yolo_annotations = convert_to_yolo_format(annotations, base_width, base_height, IMAGE_SIZE)
    
    return resized_image, yolo_annotations


def draw_texts_on_image(bg, texts, content_width, content_height, padding, line_spacing):
    """Handle text positioning and drawing with paragraph layout"""
    draw = ImageDraw.Draw(bg)
    annotations = []
    
    current_x = padding
    current_y = padding
    max_line_height = 0
    

    text_color = get_contrast_color(bg)
    
    chosen_font = get_random_font()

    for text in texts:
        # Get font and dimensions
        font, text_width, text_height = get_dynamic_font(text, chosen_font, content_width, content_height)
        
        # Check if word fits in current line
        if current_x + text_width > (bg.width - padding):
            # Move to new line
            current_x = padding
            current_y += max_line_height + line_spacing
            max_line_height = 0

        # Check if we have vertical space
        if current_y + text_height > (bg.height - padding):
            break  # No more space in the image

        # Get contrast color for this position
        
        # Draw text
        draw.text((current_x, current_y), text, fill=text_color, font=font)
        annotations.append((current_x, current_y, text_width, text_height))
        
        # Update positioning variables
        current_x += text_width + WORD_PADDING  # Add padding between words
        if text_height > max_line_height:
            max_line_height = text_height

    return bg, annotations

def prepare_base_image_and_texts(max_words):
    """Select random words and create base image"""
    texts = random.choices(TEXT_WORDS, k=max_words)
    bg = get_random_background()
    return bg, texts

def calculate_text_position(base_w, base_h, text_w, text_h):
    """Calculate random position within safe boundaries"""
    max_x = base_w - text_w
    max_y = base_h - text_h
    return (
        random.randint(0, max_x) if max_x > 0 else 0,
        random.randint(0, max_y) if max_y > 0 else 0
    )

# def get_contrast_color(image, x, y, w, h):
#     """Get color that contrasts with background region with safety checks"""
#     # Ensure crop coordinates stay within image bounds
#     x0 = max(0, x)
#     y0 = max(0, y)
#     x1 = min(image.width, x + w)
#     y1 = min(image.height, y + h)
    
#     if x0 >= x1 or y0 >= y1:
#         return (0, 0, 0)  # Fallback color
    
#     region = image.crop((x0, y0, x1, y1))
#     return contrast_color(calculate_average_color(image))
def get_contrast_color(image):
    """Get color that contrasts with background region with safety checks"""
    return contrast_color(calculate_average_color(image))

def convert_to_yolo_format(annotations, orig_w, orig_h, target_size):
    """Convert coordinates to YOLO format"""
    scale_x = target_size[0] / orig_w
    scale_y = target_size[1] / orig_h
    yolo_annotations = []
    
    for x, y, w, h in annotations:
        # Scale coordinates
        scaled = (
            x * scale_x,
            y * scale_y,
            w * scale_x,
            h * scale_y
        )
        
        # Clamp to image boundaries
        clamped = clamp_coordinates(*scaled, target_size)
        
        # Convert to YOLO format
        yolo_annotations.append(calculate_yolo_values(*clamped, target_size))
    
    return yolo_annotations

def clamp_coordinates(x, y, w, h, target_size):
    """Ensure coordinates stay within image bounds"""
    x = max(0, min(x, target_size[0] - 1))
    y = max(0, min(y, target_size[1] - 1))
    w = max(1, min(w, target_size[0] - x))
    h = max(1, min(h, target_size[1] - y))
    return (x, y, w, h)

def calculate_yolo_values(x, y, w, h, target_size):
    """Convert to YOLO normalized format"""
    x_center = (x + w/2) / target_size[0]
    y_center = (y + h/2) / target_size[1]
    width_norm = w / target_size[0]
    height_norm = h / target_size[1]
    return (0, x_center, y_center, width_norm, height_norm)








if __name__ == "__main__":
    for i in range(NUM_IMAGES):
        img, bbox = create_text_image_with_bbox()
        
        # Apply post-processing artifacts
        img = apply_artifact(img)
        
        img = adjust_brightness_contrast_alpha_beta(img)

        # Save image and label
        image_filename = f"img_{i:04d}.png"
        img.save(os.path.join(SAVE_DIR, image_filename))
        
        label_filename = f"img_{i:04d}.txt"
        with open(os.path.join(LABEL_DIR, label_filename), 'w') as f:
            for box in bbox:
                f.write(f"{box[0]} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f} {box[4]:.6f}\n")
            
        print(f"Saved {image_filename} and {label_filename}")