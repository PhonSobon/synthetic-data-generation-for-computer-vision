import numpy as np
import random
from PIL import Image
import cv2


def apply_artifact(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # if random.random() < 0.3:
    #     ksize = 3
    #     # ksize = random.choice([3, 5])
    #     img_cv = cv2.GaussianBlur(img_cv, (ksize, ksize), 0)

    if random.random() < 0.5:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(50, 80)]
        _, encimg = cv2.imencode('.jpg', img_cv, encode_param)
        img_cv = cv2.imdecode(encimg, 1)

    if random.random() < 0.3:
        size = 3
        # size = random.choice([3, 5])
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size - 1)/2), :] = np.ones(size)
        kernel_motion_blur /= size
        img_cv = cv2.filter2D(img_cv, -1, kernel_motion_blur)

    return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))



import cv2
import numpy as np
from PIL import Image

def adjust_brightness_contrast_alpha_beta(image, alpha_range=(0.8, 1.2), beta_range=(-50, 50)):
    """
    Adjust the brightness and contrast of an image using alpha (contrast) and beta (brightness).

    Args:
        image (PIL.Image.Image): The input image.
        alpha_range (tuple): Min and max multiplier for contrast adjustment.
        beta_range (tuple): Min and max value for brightness adjustment.

    Returns:
        PIL.Image.Image: The adjusted image.
    """
    # Convert PIL image to OpenCV format (numpy array)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Randomly select alpha (contrast) and beta (brightness) values
    alpha = np.random.uniform(*alpha_range)  # Contrast control
    beta = np.random.uniform(*beta_range)    # Brightness control

    # Apply the adjustments
    adjusted = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=beta)

    # Convert back to PIL format
    return Image.fromarray(cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB))