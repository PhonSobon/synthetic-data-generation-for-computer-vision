import numpy as np
import random
from PIL import Image
import cv2
import math


def apply_motion_blur(img: Image.Image, possible_size=(3, 5), posssibility=0.3) -> Image.Image:
    if random.random() < posssibility:
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        size = random.choice(possible_size)
        kernel_motion_blur = np.zeros((size, size))

        # Randomly choose horizontal or vertical motion blur
        if random.choice(["horizontal", "vertical"]) == "horizontal":
            kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
        else:
            kernel_motion_blur[:, int((size - 1) / 2)] = np.ones(size)

        # Normalize the kernel
        kernel_motion_blur /= size

        # Apply the kernel to the image
        img_cv = cv2.filter2D(img_cv, -1, kernel_motion_blur)

        return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    
    return img


def apply_artifact(img: Image.Image, possible_compression=(50, 90), posssibility=0.5) -> Image.Image:

    if random.random() < posssibility:
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Randomly choose a compression level
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 
                        random.randint(*possible_compression)]
        
        # Encode the image to apply the artifact
        _, encimg = cv2.imencode('.jpg', img_cv, encode_param)
        
        # Decode the image to apply the artifact
        img_cv = cv2.imdecode(encimg, 1)

        return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    
    return img


def rand_brightness_contrast(image: Image.Image, alpha_range=(0.8, 1.2), beta_range=(-50, 50)) -> Image.Image:
    """
    Adjust the brightness and contrast of an image using alpha (contrast) and beta (brightness).

    Args:
        image (PIL.Image.Image): The input image.
        alpha_range (tuple): Min and max multiplier for contrast adjustment.
        beta_range (tuple): Min and max value for brightness adjustment.

    Returns:
        PIL.Image.Image: The adjusted image.
    """

    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    alpha = np.random.uniform(*alpha_range)  # Contrast control
    beta = np.random.uniform(*beta_range)    # Brightness control

    adjusted = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=beta)

    return Image.fromarray(cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB))


def apply_color_jitter(
    img: Image.Image,
    possibility: float = 0.3,
    hue_delta: int = 10,
    sat_scale = (0.8, 1.2),
    val_scale = (0.8, 1.2)
) -> Image.Image:
    """
    Randomly jitter the color of `img` by moving to HSV and back.
    
    Args:
      img:        PIL image in RGB mode.
      possibility: probability [0.0-1.0] to apply jitter.
      hue_delta:   max ± shift in hue channel (0-180 scale).
      sat_scale:  (min, max) scale factor for saturation.
      val_scale:  (min, max) scale factor for value/brightness.
    
    Returns:
      A new PIL Image with color jitter applied (or the original).
    """
    if random.random() > possibility:
        return img  # no change

    arr = np.array(img.convert("RGB"), dtype=np.uint8)
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV).astype(np.int16)

    # Hue: add random between -hue_delta and +hue_delta (loop around 0–180)
    h = hsv[:, :, 0]
    h = (h + random.randint(-hue_delta, hue_delta)) % 180

    # Saturation: scale by random factor
    s = hsv[:, :, 1].astype(np.float32)
    s = np.clip(s * random.uniform(*sat_scale), 0, 255).astype(np.uint8)

    # Value: scale by random factor
    v = hsv[:, :, 2].astype(np.float32)
    v = np.clip(v * random.uniform(*val_scale), 0, 255).astype(np.uint8)

    jittered_hsv = np.stack([h, s, v], axis=2).astype(np.uint8)

    jittered_rgb = cv2.cvtColor(jittered_hsv, cv2.COLOR_HSV2RGB)

    return Image.fromarray(jittered_rgb)
