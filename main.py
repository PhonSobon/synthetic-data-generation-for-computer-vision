import os
import sys
import random
import dotenv
from PIL import ImageDraw, ImageFont, Image
from helper.image_processing import apply_artifact, rand_brightness_contrast, apply_motion_blur, apply_color_jitter
from helper.get_color import get_contrast_color
from helper.get_random import get_random_background, get_random_font, get_random_img_padding, get_random_line_spacing, get_random_word_padding, get_random_font_size
from helper.yolo_coord import convert_to_yolo_format
from helper.utils import read_text_file, save_label, save_xml_label
from helper.xml_generator import generate_xml_content
from helper.khnormal import khnormal


dotenv.load_dotenv()


# === CONFIGURATION ===

# A4 PAGE SIZE AT 300 DPI (8.27 x 11.69 inches)
# At 300 DPI: width = 2480px, height = 3508px
# At 200 DPI: width = 1654px, height = 2339px
DPI = int(os.getenv("DPI", 300))
A4_WIDTH_INCHES = 8.27
A4_HEIGHT_INCHES = 5.69

# Calculate image size based on DPI
IMAGE_WIDTH = int(A4_WIDTH_INCHES * DPI)
IMAGE_HEIGHT = int(A4_HEIGHT_INCHES * DPI)
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

# MARGINS (converted to pixels based on DPI)
# Top: 0.6 inches (1.5 cm)
# Bottom: 0.6 inches (1.5 cm)
# Left: 0.78 inches (2 cm)
# Right: 0.6 inches (1.5 cm)
TOP_MARGIN_INCHES = float(os.getenv("TOP_MARGIN_INCHES", 0.6))
BOTTOM_MARGIN_INCHES = float(os.getenv("BOTTOM_MARGIN_INCHES", 0.6))
LEFT_MARGIN_INCHES = float(os.getenv("LEFT_MARGIN_INCHES", 0.78))
RIGHT_MARGIN_INCHES = float(os.getenv("RIGHT_MARGIN_INCHES", 0.6))

# Convert margins to pixels
TOP_MARGIN_PX = int(TOP_MARGIN_INCHES * DPI)
BOTTOM_MARGIN_PX = int(BOTTOM_MARGIN_INCHES * DPI)
LEFT_MARGIN_PX = int(LEFT_MARGIN_INCHES * DPI)
RIGHT_MARGIN_PX = int(RIGHT_MARGIN_INCHES * DPI)

# IMAGE SCALE
MIN_IMG_SCALE = float(os.getenv("MIN_IMG_SCALE", 0.5))
MAX_IMG_SCALE = float(os.getenv("MAX_IMG_SCALE", 2.0))

# DIRECTORIES
FONT_DIR = os.getenv("FONT_DIR", "fonts/")
SAVE_DIR = os.getenv("SAVE_DIR", "synthetic_images/")
LABEL_DIR = os.getenv("LABEL_DIR", "synthetic_labels/")
XML_DIR = os.getenv("XML_DIR", "synthetic_xml_labels/")
BACKGROUND_IMAGES_DIR = os.getenv("BACKGROUND_IMAGES_DIR", {"white": "#ffffff"})

# FONT SIZE (typical document font: 11-12pt at 300 DPI ≈ 44-48px)
# For 12pt font at 300 DPI: 12 * 300/72 = 50px
FONT_SIZE_PT = int(os.getenv("FONT_SIZE_PT", 12))
FONT_SIZE_PX = int(FONT_SIZE_PT * DPI / 72)

MIN_FONT_SIZE = int(os.getenv("MIN_FONT_SIZE", FONT_SIZE_PX))
MAX_FONT_SIZE = int(os.getenv("MAX_FONT_SIZE", FONT_SIZE_PX))

# IMAGE PADDING (use calculated margins)
MIN_IMG_PADDING = LEFT_MARGIN_PX
MAX_IMG_PADDING = LEFT_MARGIN_PX

# LINE SPACING
# Single spacing (1.0) = font size
# For paragraph spacing: 6pt at 300 DPI = 6 * 300/72 = 25px
PARAGRAPH_SPACING_PT = float(os.getenv("PARAGRAPH_SPACING_PT", 6))
PARAGRAPH_SPACING_PX = int(PARAGRAPH_SPACING_PT * DPI / 72)

# Line spacing = 1.0 (single space) means spacing = font_size
LINE_SPACING_MULTIPLIER = float(os.getenv("LINE_SPACING_MULTIPLIER", 1.0))
LINE_SPACING_PX = int(FONT_SIZE_PX * LINE_SPACING_MULTIPLIER)

MIN_LINE_SPACING = int(os.getenv("MIN_LINE_SPACING", LINE_SPACING_PX))
MAX_LINE_SPACING = int(os.getenv("MAX_LINE_SPACING", LINE_SPACING_PX))

# WORD PADDING
MIN_WORD_PADDING = int(os.getenv("MIN_WORD_PADDING", 2))
MAX_WORD_PADDING = int(os.getenv("MAX_WORD_PADDING", 10))

# TEXT FILE
TEXT_FILE = os.getenv("TEXT_FILE", "combine_clean.txt")
USE_SPECIFIC_TEXT = os.getenv("USE_SPECIFIC_TEXT", "false").lower() == "true"
SPECIFIC_TEXT_FILE = os.getenv("SPECIFIC_TEXT_FILE", "specific_text.txt")

# PARAGRAPH LENGTH
MIN_PARAG_LENGTH = int(os.getenv("MIN_PARAG_LENGTH", 100))
MAX_PARAG_LENGTH = int(os.getenv("MAX_PARAG_LENGTH", 200))

# BOUNDING BOX PADDING
BBOX_WIDTH_PADDING = int(os.getenv("BBOX_WIDTH_PADDING", 1))
BBOX_HEIGHT_PADDING = int(os.getenv("BBOX_HEIGHT_PADDING", 2))

# ARTIFACTS
ARTIFACT_POSSIBILITIES = float(os.getenv("ARTIFACT_POSSIBILITIES", 0.5))
jpeg_compression_range_str = os.getenv("JPEG_COMPRESSION_RANGE", "50,90")
JPEG_COMPRESSION_RANGE = tuple(map(int, jpeg_compression_range_str.split(',')))

# MOTION BLUR
MOTION_BLUR_POSSIBILITIES = float(os.getenv("MOTION_BLUR_POSSIBILITIES", 0.3))
motion_blur_kernel_size_str = os.getenv("MOTION_BLUR_KERNEL_SIZE_RANGE", "3,3")
MOTION_BLUR_KERNEL_SIZE_RANGE = tuple(map(int, motion_blur_kernel_size_str.split(',')))

# BRIGHTNESS ADJUSTMENT
alpha_range_str = os.getenv("ALPHA_RANGE", "0.8,1.2")
ALPHA_RANGE = tuple(map(float, alpha_range_str.split(',')))

beta_range_str = os.getenv("BETA_RANGE", "-50,50")
BETA_RANGE = tuple(map(int, beta_range_str.split(',')))

# COLOR JITTER SETTINGS
COLOR_JITTER_POSSIBILITES = float(os.getenv("COLOR_JITTER_POSSIBILITES", 0.3))
HUE_DELTA = int(os.getenv("HUE_DELTA", 10))

sat_scale_str = os.getenv("SAT_SCALE", "0.8,1.2")
SAT_SCALE = tuple(map(float, sat_scale_str.split(',')))

val_scale_str = os.getenv("VAL_SCALE", "0.8,1.2")
VAL_SCALE = tuple(map(float, val_scale_str.split(',')))

MAX_ROTATION = float(os.getenv("MAX_ROTATION", "5.0"))

# POSSIBILITIES FOR VARIATIONS
POSSIBILITIES_FOR_NEW_PADDING = float(os.getenv("POSSIBILITIES_FOR_NEW_PADDING", 0.005))
POSSIBILITIES_FOR_NEW_LINE_SPACING = float(os.getenv("POSSIBILITIES_FOR_NEW_LINE_SPACING", 0.005))
POSSIBILITIES_FOR_NEW_WORD_PADDING = float(os.getenv("POSSIBILITIES_FOR_NEW_WORD_PADDING", 0.005))
POSSIBILITIES_FOR_NEW_FONT_SIZE = float(os.getenv("POSSIBILITIES_FOR_NEW_FONT_SIZE", 0.005))
POSSIBILITIES_FOR_NEW_FONT = float(os.getenv("POSSIBILITIES_FOR_NEW_FONT", 0.005))

POSSIBILITIES_FOR_NEW_Y = float(os.getenv("POSSIBILITIES_FOR_NEW_Y", 0.005))
new_y_range_str = os.getenv("NEW_Y_RANGE", "-5,10")
new_y_range_list = list(map(int, new_y_range_str.split(',')))[:2]
NEW_Y_RANGE = new_y_range_list[0], new_y_range_list[1]

POSSIBILITIES_FOR_NEW_X = float(os.getenv("POSSIBILITIES_FOR_NEW_X", 0.005))
new_x_range_str = os.getenv("NEW_X_RANGE", "-5,10")
new_x_range_list = list(map(int, new_x_range_str.split(',')))[:2]
NEW_X_RANGE = new_x_range_list[0], new_x_range_list[1]

POSSIBILITIES_FOR_NEW_COLOR = float(os.getenv("POSSIBILITIES_FOR_NEW_COLOR", 0.005))

# === END CONFIGURATION ===


def load_specific_texts() -> list[str]:
    """Load specific text from file, with each line being one text sample"""
    if not os.path.exists(SPECIFIC_TEXT_FILE):
        print(f"Warning: {SPECIFIC_TEXT_FILE} not found. Creating example file.")
        with open(SPECIFIC_TEXT_FILE, 'w', encoding='utf-8') as f:
            f.write("ឃាត់ជនសង្ស័យម្នាក់បន្ទាប់ពីធ្វើសកម្មភាពលួចយកកាបូបលុយជនរងគ្រោះ\n")
            f.write("នេះជាឧទាហរណ៍នៃអត្ថបទភាសាខ្មែរ\n")
    
    return read_text_file(SPECIFIC_TEXT_FILE)


def create_text_image_with_bbox(specific_text: str = None, word_list: list[str] = None, start_idx: int = 0) -> tuple[Image.Image, list[list[tuple[str, tuple[float, float, float, float]]]], list[tuple[float, float, float, float]], int]:
    """Create an image with text and bounding boxes
    
    Returns: (image, lines, annotations, next_start_idx)
    """

    if specific_text:
        texts = specific_text.split()
        next_idx = start_idx
    elif word_list is not None:
        text_len = random.randint(MIN_PARAG_LENGTH, MAX_PARAG_LENGTH)
        end_idx = min(start_idx + text_len, len(word_list))
        texts = word_list[start_idx:end_idx]
        next_idx = end_idx if end_idx < len(word_list) else 0
    else:
        TEXT_WORDS = read_text_file(TEXT_FILE)
        text_len = random.randint(MIN_PARAG_LENGTH, MAX_PARAG_LENGTH)
        texts = random.choices(TEXT_WORDS, k=text_len)
        next_idx = start_idx

    # CRITICAL: Normalize each word individually to preserve word boundaries
    texts = ["".join(khnormal(text)) for text in texts]

    bg = get_random_background(IMAGE_SIZE, BACKGROUND_IMAGES_DIR, MIN_IMG_SCALE, MAX_IMG_SCALE)

    drawn_image, lines, annotations = draw_texts_on_image(
        bg,
        texts,
        FONT_DIR,
        MIN_IMG_PADDING,
        MAX_IMG_PADDING,
        MIN_LINE_SPACING,
        MAX_LINE_SPACING,
        MIN_FONT_SIZE,
        MAX_FONT_SIZE,
        MIN_WORD_PADDING,
        MAX_WORD_PADDING,
        POSSIBILITIES_FOR_NEW_PADDING,
        POSSIBILITIES_FOR_NEW_LINE_SPACING,
        POSSIBILITIES_FOR_NEW_WORD_PADDING,
        POSSIBILITIES_FOR_NEW_FONT_SIZE,
        POSSIBILITIES_FOR_NEW_FONT,
        POSSIBILITIES_FOR_NEW_Y, NEW_Y_RANGE,
        POSSIBILITIES_FOR_NEW_X, NEW_X_RANGE,
        POSSIBILITIES_FOR_NEW_COLOR,
        BBOX_WIDTH_PADDING, BBOX_HEIGHT_PADDING,
    )

    return drawn_image, lines, annotations, next_idx


def draw_texts_on_image(
    bg: Image.Image,
    texts: list[str],
    font_dir: str,
    min_img_padding: int,
    max_img_padding: int,
    min_line_spacing: int,
    max_line_spacing: int,
    min_font_size: int,
    max_font_size: int,
    min_word_padding: int,
    max_word_padding: int,
    possibilities_for_new_padding: float,
    possibilities_for_new_line_spacing: float,
    possibilities_for_new_word_padding: float,
    possibilities_for_new_font_size: float,
    possibilities_for_new_font: float,
    possibilities_for_new_y: float, new_y_range: tuple[int, int],
    possibilities_for_new_x: float, new_x_range: tuple[int, int],
    possibilities_for_new_color: float,
    bbox_width_padding: int, bbox_height_padding: int,
) -> tuple[Image.Image, list[list[tuple[str, tuple[float, float, float, float]]]], list[tuple[float, float, float, float]]]:
    """
    Draws words continuously (no spaces) onto bg with A4 margins and spacing.
    """

    # Use fixed margins instead of random padding
    x_padding_left = LEFT_MARGIN_PX
    x_padding_right = RIGHT_MARGIN_PX
    y_padding_top = TOP_MARGIN_PX
    y_padding_bottom = BOTTOM_MARGIN_PX
    
    # Use single line spacing (1.0)
    line_spacing = LINE_SPACING_PX
    
    # Use fixed font size (12pt by default)
    font_size = FONT_SIZE_PX

    chosen_font_path = get_random_font(font_dir)
    font = ImageFont.truetype(chosen_font_path, font_size)
    
    draw = ImageDraw.Draw(bg)
    annotations = []
    current_line = []
    lines = []

    current_x = x_padding_left
    current_y = y_padding_top
    max_line_height = 0

    text_color = get_contrast_color(bg, 0, 0, bg.width, bg.height)
    
    # Calculate usable width (page width minus left and right margins)
    usable_width = bg.width - x_padding_left - x_padding_right

    for word in texts:
        if random.random() < possibilities_for_new_font:
            chosen_font_path = get_random_font(font_dir)
            font = ImageFont.truetype(chosen_font_path, font_size)
        if random.random() < possibilities_for_new_y:
            current_y += random.randint(*new_y_range)
        if random.random() < possibilities_for_new_x:
            current_x += random.randint(*new_x_range)
        if random.random() < possibilities_for_new_color:
            text_color = get_contrast_color(bg, 0, 0, bg.width, bg.height)

        bbox = font.getbbox(word)
        left, top, right, bottom = bbox
        text_width = right - left
        text_height = bottom - top

        # Check if word fits on current line (respect right margin)
        if current_x + text_width > (bg.width - x_padding_right):
            if current_line:
                lines.append(current_line)
                current_line = []
            current_x = x_padding_left
            current_y += max_line_height + line_spacing
            max_line_height = 0

        # Check vertical space (respect bottom margin)
        if current_y + text_height > (bg.height - y_padding_bottom):
            break

        # Draw the word
        draw.text((current_x, current_y), word, font=font, fill=text_color)
        
        # Calculate bounding box with padding
        x = current_x + left - bbox_width_padding
        y = current_y + top - bbox_height_padding
        text_width_padded = text_width + 2 * bbox_width_padding
        text_height_padded = text_height + 2 * bbox_height_padding

        word_info = (word, (x, y, text_width_padded, text_height_padded))
        current_line.append(word_info)
        annotations.append((x, y, text_width_padded, text_height_padded))

        # Move cursor WITHOUT spacing (continuous text)
        current_x += (right - left)
        max_line_height = max(max_line_height, (bottom - top))

    if current_line:
        lines.append(current_line)

    return bg, lines, annotations


if __name__ == "__main__":
    sys.argv = sys.argv[1:]

    _from = int(sys.argv[0])
    _to = int(sys.argv[1])
    _step = int(sys.argv[2])

    specific_texts = None
    word_list = None
    current_word_idx = 0
    
    if USE_SPECIFIC_TEXT:
        specific_texts = load_specific_texts()
        print(f"Loaded {len(specific_texts)} specific text samples")
    else:
        word_list = read_text_file(TEXT_FILE)
        print(f"Loaded {len(word_list)} words from {TEXT_FILE}")
        print(f"Using words sequentially (not randomly)")

    for i in range(_from, _to, _step):
        if specific_texts:
            text_idx = i % len(specific_texts)
            current_text = specific_texts[text_idx]
            img, lines, bbox, _ = create_text_image_with_bbox(specific_text=current_text)
            print(f"Generating image {i} with text: {current_text[:50]}...")
        elif word_list:
            img, lines, bbox, current_word_idx = create_text_image_with_bbox(
                word_list=word_list, 
                start_idx=current_word_idx
            )
            words_used = sum(len(line) for line in lines)
            print(f"Image {i}: Used {words_used} words starting from index {current_word_idx - words_used}")
        else:
            img, lines, bbox, _ = create_text_image_with_bbox()

        img = apply_artifact(img, posssibility=ARTIFACT_POSSIBILITIES,
                             possible_compression=JPEG_COMPRESSION_RANGE)
        img = apply_motion_blur(img, posssibility=MOTION_BLUR_POSSIBILITIES,
                                possible_size=MOTION_BLUR_KERNEL_SIZE_RANGE)
        img = rand_brightness_contrast(
            img, alpha_range=ALPHA_RANGE, beta_range=BETA_RANGE)
        img = apply_color_jitter(img, possibility=COLOR_JITTER_POSSIBILITES, 
                                 hue_delta=HUE_DELTA, sat_scale=SAT_SCALE, val_scale=VAL_SCALE)

        bbox = convert_to_yolo_format(bbox, img.width, img.height, IMAGE_SIZE)
        
        os.makedirs(SAVE_DIR, exist_ok=True)
        os.makedirs(LABEL_DIR, exist_ok=True)
        os.makedirs(XML_DIR, exist_ok=True)

        image_filename = f"img_{i:05d}.png"
        img.save(os.path.join(SAVE_DIR, image_filename))

        label_filename = f"img_{i:05d}.txt"
        save_label(bbox, os.path.join(LABEL_DIR, label_filename))

        xml_content = generate_xml_content(
            lines=lines,
            image_filename=image_filename,
            image_size=img.size
        )

        xml_filename = f"img_{i:05d}.xml"
        save_xml_label(xml_content, os.path.join(XML_DIR, xml_filename))

        print(f"Saved {image_filename} and {label_filename} and {xml_filename}")