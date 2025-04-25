# helper/calculation.py
import numpy as np

def calculate_transformed_bbox(original_bbox, transform_params):
    x1, y1, x2, y2 = original_bbox
    points = np.array([
        [x1, y1, 1],
        [x2, y1, 1],
        [x2, y2, 1],
        [x1, y2, 1]
    ])
    
    # Create transformation matrix
    a, b, c = transform_params['scale'][0], transform_params['shear'][0], transform_params['translate'][0]
    d, e, f = transform_params['shear'][1], transform_params['scale'][1], transform_params['translate'][1]
    matrix = np.array([
        [a, b, c],
        [d, e, f],
        [0, 0, 1]
    ])
    
    # Transform points
    transformed = points @ matrix.T
    
    # Get min/max coordinates
    xs = transformed[:, 0]
    ys = transformed[:, 1]
    return (
        np.min(xs).item(),
        np.min(ys).item(),
        np.max(xs).item(),
        np.max(ys).item()
    )

def calculate_average_color(img):
    img = img.convert("RGB")
    img_array = np.array(img)
    avg_color = img_array.mean(axis=(0, 1))
    return tuple(avg_color.astype(int))
