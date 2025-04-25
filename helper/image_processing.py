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



def apply_text_transform(text_layer):
    # Random affine transformation matrix
    transform_params = {
        'scale': (random.uniform(0.8, 1.2), random.uniform(0.8, 1.2)),
        'shear': (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
        'translate': (random.randint(-5, 5), random.randint(-5, 5))
    }
    
    # Apply transformation
    transformed = text_layer.transform(
        text_layer.size,
        Image.Transform.AFFINE,
        [
            transform_params['scale'][0],  # x-scale
            transform_params['shear'][0],  # x-shear
            transform_params['translate'][0],
            transform_params['shear'][1],  # y-shear
            transform_params['scale'][1],  # y-scale
            transform_params['translate'][1]
        ],
        resample=Image.Resampling.BILINEAR
    )
    
    return transformed, transform_params
