import numpy as np


def calculate_average_color(img):
    img = img.convert("RGB")
    img_array = np.array(img)
    avg_color = img_array.mean(axis=(0, 1))
    return tuple(avg_color.astype(int))
