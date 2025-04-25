
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        test_width = bbox[2] - bbox[0]

        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))
    return lines


def wrap_words(text, font, max_width, padding):
    """Wrap words with individual bounding boxes"""
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        bbox = font.getbbox(word)
        word_width = bbox[2] - bbox[0]
        
        if current_width + word_width > max_width - 2*padding:
            lines.append(current_line)
            current_line = []
            current_width = 0
            
        current_line.append((word, word_width))
        current_width += word_width + 10  # Add spacing
        
    if current_line:
        lines.append(current_line)
    return lines