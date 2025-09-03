import re


def clean_khmer_text(text):
    # Define a regex pattern to match Khmer characters
    # Unicode range for Khmer: \u1780-\u17FF
    # Remove everything that is not Khmer characters or spaces
    cleaned_text = re.sub(r'[^\u1780-\u17FF\s]', '', text)
    return cleaned_text


# Example usage
if __name__ == "__main__":
    with open('utils/oscar_kh_1.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = clean_khmer_text(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.split(sep=" ")

    text = set(text)

    with open('oscar_kh_1_cleaned.txt', 'w', encoding='utf-8') as nfile:
        for word in text:
            nfile.write(word+"\n")
    print("Cleaned text saved to 'oscar_kh_1_cleaned.txt'")