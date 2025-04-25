from helper.calculation import calculate_average_color

def contrast_color(bg_color):
    bg_r, bg_g, bg_b = bg_color
    brightness = (bg_r * 299 + bg_g * 587 + bg_b * 114) / 1000
    return (0, 0, 0, 255) if brightness > 160 else (255, 255, 255, 255)

# helper/get_color.py
def get_word_color(background_patch):
    # Calculate color based on actual text position background
    avg_color = calculate_average_color(background_patch)
    return contrast_color(avg_color)