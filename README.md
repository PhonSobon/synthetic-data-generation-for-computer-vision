# 📚 Synthetic Data Generator for Khmer Word Detection

This project helps you **create high-quality synthetic data** for training **YOLO object detection models** to detect **Khmer words**.  
It automatically generates **images**, **YOLO format labels**, and **Pascal VOC XML labels**.

---

## ✨ Features

- ✅ 50+ different real background images.
- ✅ Unlimited background colors (random RGB values).
- ✅ 250+ different Khmer fonts.
- ✅ Random brightness, contrast, color jitter, and motion blur.
- ✅ Random text sizes, line spacings, paddings, and positions.
- ✅ Both **YOLO** `.txt` and **Pascal VOC** `.xml` label formats.
- ✅ Easy-to-customize with `.env` configuration file.

---

## Pre-Generated Dataset

You can find a pre-generated dataset on Kaggle with default configuration for 100K images.
You can use it here: [Dataset](https://www.kaggle.com/datasets/veasnaecevilsna/synthetic-data-for-khmer-word-detection)

## 🏗️ How It Works

The generator randomly:

1. Picks a background (real image or random color).
2. Picks a random Khmer font.
3. Picks random words from a large Khmer text file.
4. Places the words onto the background with random styles (font size, padding, line spacing, color).
5. Applies random image effects (like blur, brightness change, etc.).
6. Saves:
   - The **generated image** (as `.png`).
   - The **bounding boxes** (as `.txt` for YOLO and `.xml` for Pascal VOC).

---

## 🛠️ Installation

```bash
git clone https://github.com/Chanveasna-ENG/synthetic-data-generation-for-computer-vision.git
cd synthetic-data-generation-for-computer-vision
pip install -r requirements.txt
```

On Linux sometimes you need to install libgl1 for opencv

```bash
sudo apt update
sudo apt install -y libgl1
```

> **Note:** You also need to place your background images and Khmer fonts into the proper folders!

---

## 📂 Project Structure

```plaintext
/
├── background/            # Background images
├── example_images/        # Example images
├── fonts/                 # Khmer fonts
├── helper/                # Helper functions (image processing, color, random utils, etc.)
├── utils/                 # Contain the original khmer text data and a cleaning function
├── synthetic_images/      # Generated images will be saved here
├── synthetic_labels/      # YOLO labels (.txt)
├── synthetic_xml_labels/  # Pascal VOC labels (.xml)
├── .env                   # Config file (image size, font size range, etc.)
├── .gitignore             # Ignore unrelated files
├── font_test.py           # It will test the khmer font find corrupt fonts (or unsupported by your system) and generate sample of that font.
├── main.py                # Main script to create synthetic images
├── oscar_kh_1_cleaned.txt # Main text file contain unique khmer words for randomized
├── README.md              # (this file)
├── requirements.txt        # Dependencies for the project
└── test.ipynb             # Jupyter notebook for testing and visualization
```

---

## ⚙️ Configuration (.env)

You can change settings easily in the `.env` file!

Example:

```dotenv
IMAGE_SIZE=775,550
MIN_FONT_SIZE=20
MAX_FONT_SIZE=100
BACKGROUND_IMAGES_DIR=background/
FONT_DIR=fonts/
SAVE_DIR=synthetic_images/
LABEL_DIR=synthetic_labels/
XML_DIR=synthetic_xml_labels/
TEXT_FILE=oscar_kh_1_cleaned.txt
MIN_PARAG_LENGTH=1
MAX_PARAG_LENGTH=500
```

Some important options you can control:

| Option                    | Description                                           |
| ------------------------- | ----------------------------------------------------- |
| IMAGE_SIZE                | Width, Height of generated images                     |
| MIN/MAX_FONT_SIZE         | Font size range                                       |
| BACKGROUND_IMAGES_DIR     | Where backgrounds are stored                         |
| FONT_DIR                  | Where fonts are stored                               |
| TEXT_FILE                 | Text file containing Khmer words                     |
| ARTIFACT_POSSIBILITIES    | Chance of adding JPEG noise                          |
| MOTION_BLUR_POSSIBILITIES | Chance of adding motion blur                         |
| COLOR_JITTER_POSSIBILITIES| Chance of color change (Hue, Saturation, Brightness)  |

---

## 🧠 Example Usage

Here’s how you create one hundred synthetic image with labels:

```bash
python3 main.py 0 100 1
```

The code here is working like python loop. 

- "0" is the starting index
- "100" is the ending index
- "1" is the step

---

## 🖼️ Example Output

### Images

![sample image](https://github.com/Chanveasna-ENG/synthetic-data-generation-for-computer-vision/blob/main/example_images/img_00000.png) 

### YOLO Labels

```plaintext
0 0.235265 0.051601 0.144401 0.081851
0 0.371316 0.052195 0.123772 0.052195
0 0.528487 0.055753 0.186640 0.073547
0 0.686149 0.048636 0.124754 0.056940
0 0.776523 0.068209 0.052063 0.084223
0 0.153733 0.163108 0.124754 0.069988
```

### XML Label

```xml

<?xml version='1.0' encoding='utf-8'?>
<metadata>
  <image>img_00000.png</image>
  <width>1018</width>
  <height>843</height>
  <paragraph>
    <line id="1">
      <word>
        <text>ត្រុន</text>
        <bbox x1="93" y1="28" x2="164" y2="79" />
      </word>
      <word>
        <text>ការកៀក</text>
        <bbox x1="166" y1="9" x2="313" y2="78" />
      </word>
      <word>
        <text>រលោង</text>
        <bbox x1="315" y1="22" x2="441" y2="66" />
      </word>
      <word>
        <text>ដើម្បីឱ្យដឹង</text>
        <bbox x1="443" y1="16" x2="633" y2="78" />
      </word>
      <word>
        <text>ការដើរ</text>
        <bbox x1="635" y1="17" x2="762" y2="65" />
      </word>
      <word>
        <text>ឃ្មុំ</text>
        <bbox x1="764" y1="22" x2="817" y2="93" />
      </word>
    </line>
    </paragraph>
</metadata>
```

### Example from test.ipynb

![sample image](https://github.com/Chanveasna-ENG/synthetic-data-generation-for-computer-vision/blob/main/example_images/image_2025-04-29_09-07-58.png) 

---

## 🚀 Future Plans

- Add more realistic distortions (e.g., handwriting simulation).
- Automatically mix real-world photos and synthetic text.
- Generate rotated bounding boxes (for skewed text).

---

## ❤️ Credits

- Khmer Text were collected from this [khmer-text-data](https://github.com/phylypo/khmer-text-data/)
- Khmer fonts were collected from free and open sources.
You can find the font here: [Khmer Fonts](https://sourceforge.net/projects/khmer-open-source/)
- Backgrounds were curated for synthetic data purposes.
- Khmer Normalizer code were collected from [Khnormal](https://github.com/sillsdev/khmer-character-specification/blob/master/python/scripts/khnormal)
- Khmer Dictionary 2022 were collected from [Hugging Face: Khmer Dictionary 44k](https://huggingface.co/datasets/seanghay/khmer-dictionary-44k)

---

## Useful Resources

- [Khmer word Normalizer](https://normalize.ភាសាខ្មែរ.com/)
- [Khmer Encoding structure IDRI EDU](https://www.idri.edu.kh/research/khmer-encoding-structure/)

---

## 📜 License

This project is **free to use** for research, personal, and educational purposes.  
For commercial use, please contact the author.

Please give credit to the original authors when using this data and give link to this repository.

---

# ✉️ Contact

If you have any questions or want to collaborate, feel free to reach out:

- 📧 Email: veasnaec@gmail.com
- 🌐 GitHub: [Chanveasna ENG](https://github.com/Chanveasna-ENG)

---
