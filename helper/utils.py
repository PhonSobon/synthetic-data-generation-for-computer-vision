def read_text_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read().splitlines()


def save_label(bbox: list[tuple[int, float, float, float, float]], filename: str) -> None:
    """Save the label to the specified filename."""
    with open(filename, 'w') as f:
        for b in bbox:
            entry = f"{b[0]} {b[1]:.6f} {b[2]:.6f} {b[3]:.6f} {b[4]:.6f}\n"
            f.write(entry)


def save_xml_label(xml_content: str, xml_filename: str) -> None:
    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(xml_content)
