
def convert_to_yolo_format(annotations: list[tuple[float, float, float, float]], orig_w: int, orig_h: int, target_size: tuple[int, int]) -> list[tuple[int, float, float, float, float]]:
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


def clamp_coordinates(x: float, y: float, w: float, h: float, target_size: tuple[int, int]) -> tuple[float, float, float, float]:
    """Ensure coordinates stay within image bounds"""
    x = max(0, min(x, target_size[0] - 1))
    y = max(0, min(y, target_size[1] - 1))
    w = max(1, min(w, target_size[0] - x))
    h = max(1, min(h, target_size[1] - y))
    return (x, y, w, h)


def calculate_yolo_values(x: float, y: float, w: float, h: float, target_size: tuple[int, int]) -> tuple[int, float, float, float, float]:
    """Convert to YOLO normalized format"""
    x_center = (x + w / 2) / target_size[0]
    y_center = (y + h / 2) / target_size[1]
    width_norm = w / target_size[0]
    height_norm = h / target_size[1]
    return (0, x_center, y_center, width_norm, height_norm)
