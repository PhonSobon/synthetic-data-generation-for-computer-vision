# helper/xml_generator.py
import xml.etree.ElementTree as ET
from typing import List, Tuple

def generate_xml_content(
    lines: List[List[Tuple[str, Tuple]]], 
    image_filename: str, 
    image_size: Tuple[int, int]
) -> str:
    """
    Generate XML content in the specified format
    Args:
        lines: List of lines containing word tuples (text, (x, y, w, h))
        image_filename: Name of the image file
        image_size: Tuple of (width, height)
    """
    root = ET.Element("metadata")
    
    # Image info
    ET.SubElement(root, "image").text = image_filename
    ET.SubElement(root, "width").text = str(image_size[0])
    ET.SubElement(root, "height").text = str(image_size[1])
    
    # Main paragraph container
    paragraph = ET.SubElement(root, "paragraph")
    
    # Add lines with words
    for line_id, line in enumerate(lines, 1):
        line_elem = ET.SubElement(paragraph, "line", id=str(line_id))
        
        for word_idx, (word_text, bbox) in enumerate(line):
            word_elem = ET.SubElement(line_elem, "word")
            
            # Word text
            ET.SubElement(word_elem, "text").text = word_text
            
            # Bounding box coordinates
            x1, y1, w, h = bbox
            bbox_elem = ET.SubElement(word_elem, "bbox")
            bbox_elem.set("x1", str(round(x1)))
            bbox_elem.set("y1", str(round(y1)))
            bbox_elem.set("x2", str(round(x1 + w)))
            bbox_elem.set("y2", str(round(y1 + h)))
    
    # Format XML
    ET.indent(root, space="  ")
    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode()
    return f"<?xml version='1.0' encoding='utf-8'?>\n{xml_str}"