import os
from PIL import Image, ImageDraw, ImageFont

def test_fonts(font_dir, output_dir):
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    corrupt_fonts = []
    valid_fonts = []
    
    for font_file in os.listdir(font_dir):
        if font_file.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(font_dir, font_file)
            font_name = os.path.splitext(font_file)[0]
            output_path = os.path.join(output_dir, f"{font_name}.png")
            
            try:
                # Try loading the font
                font = ImageFont.truetype(font_path, 40)
                
                # Create simple image with font name
                img = Image.new('RGB', (800, 200), color='white') # type: ignore
                d = ImageDraw.Draw(img)
                
                # Draw text
                d.text((10, 50), "រដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជាគឺជាច្បាប់កំពូល។", font=font, fill='black')
                
                # Save image
                img.save(output_path)
                valid_fonts.append(font_file)
                
            except Exception as e:
                corrupt_fonts.append(font_file)
                print(f"Corrupt font: {font_file} - {str(e)}")
    
    # Print summary
    print("\nTest complete:")
    print(f"Valid fonts: {len(valid_fonts)}")
    print(f"Corrupt fonts: {len(corrupt_fonts)}")
    if corrupt_fonts:
        print("\nCorrupt font files:")
        for f in corrupt_fonts:
            print(f" - {f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test font files and generate samples')
    parser.add_argument('--font-dir', default='fonts', help='Directory containing font files')
    parser.add_argument('--output-dir', default='font_test_output', help='Output directory for sample images')
    
    args = parser.parse_args()
    
    test_fonts(args.font_dir, args.output_dir)