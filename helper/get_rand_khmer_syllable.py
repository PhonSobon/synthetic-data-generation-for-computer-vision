# --- 1. BASE CHARACTERS ---
# These are the foundation of any syllable. A syllable MUST start with one of these. [cite: 82, 130]
consonants_a_series = [
    'ក', 'ខ', 'ច', 'ឆ', 'ដ', 'ឋ', 'ណ', 'ត', 'ថ', 'ប', 'ផ', 'ស', 'ហ', 'អ'
]

consonants_o_series = [
    'គ', 'ឃ', 'ង', 'ជ', 'ឈ', 'ញ', 'ឌ', 'ឍ', 'ទ', 'ធ', 'ន', 'ព', 'ភ', 'ម', 'យ', 'រ', 'ល', 'វ'
]

# This consonant cannot form a subscript. [cite: 74]
consonant_no_subscript = 'ឡ'


# Independent vowels also function as Base characters. [cite: 82]
# I've used the list from the PDF, excluding the deprecated ones as you suggested. [cite: 75, 76, 79]
independent_vowels = [
    'ឥ', 'ឦ', 'ឧ', 'ឩ', 'ឪ', 'ឫ', 'ឬ', 'ឭ', 'ឮ', 'ឯ', 'ឰ', 'ឱ', 'ឲ', 'ឳ'
]


# --- 2. COENG-FORMER (Control Character) ---
# This is the invisible character that turns the next consonant into a subscript. [cite: 83, 171]
COENG = '្'


# --- 3. DEPENDENT VOWELS ---
# These modify the vowel sound of the base consonant. [cite: 88]
dependent_vowels = [
    'ា', 'ិ', 'ី', 'ឹ', 'ឺ', 'ុ', 'ូ', 'ួ', 'ើ', 'ឿ', 'ៀ', 'េ', 'ែ', 'ៃ', 'ោ', 'ៅ'
]


# --- 4. SHIFTERS ---
# These change a consonant's series from a-series to o-series or vice-versa. [cite: 93]
# They are placed after the entire consonant cluster (Base + Coengs). [cite: 181, 182]
# shifters = [
#     '៉', # MUUSIKATOAN (U+17C9): Shifts o-series to a-series. [cite: 94]
#     '៊'  # TRIISAP (U+17CA): Shifts a-series to o-series. [cite: 95]
# ]
shifters = {'o_to_a': '៉', 'a_to_o': '៊'}

# --- 5. MODIFIERS (Diacritics) ---
# These are non-spacing marks that further modify the sound. [cite: 97, 198]

# ROBAT is special. It MUST be placed immediately after the base consonant, before any coeng. [cite: 100, 167]
robat = '៌' # ROBAT (U+17CC) [cite: 78]

# Other common modifiers. They are placed after the vowel sign. [cite: 198]
modifiers = [
    'ំ', # NIKAHIT (U+17C6) [cite: 77]
    '់', # BANTOC (U+17CB) [cite: 78]
    '៍', # TOANDAKHIAT (U+17CD) [cite: 78]
    '៏', # KAKABAT (U+17CE) [cite: 78]
    '័', # AHSDA (U+17CF) [cite: 78]
    '៎', # SAMYOK SANNYA (U+17D0) [cite: 78]
    #'៑'  # VIRIAM (U+17D1) [cite: 78]
]


# --- 6. FINAL SPACING SIGNS ---
# These are spacing characters that appear at the very end of a syllable. [cite: 102, 199]
final_signs = [
    'ះ', # REAHMUK (U+17C7) [cite: 78]
    'ៈ'  # YUUKALEAPINTU (U+17C8) [cite: 78]
]


# --- 7. OTHER CHARACTERS (Standalone) ---
# These are not part of the core syllable structure. [cite: 104]

# Your list was pretty good, I just added the ones from the Unicode chart in the PDF. [cite: 78, 79]
punctuations = [
    '។', # KHAN [cite: 78]
    '៕', # BARIYOOSAN [cite: 79]
    '៖', # CAMNUC PII KUUH [cite: 79]
    '៘', # BATHAMASAT (Marked as deprecated in favor of U+19E0, but good to have) [cite: 79]
    '៙', # KHMER SIGN BARIYOOSAN (also from your list)
    '៚'  # KHMER SIGN CAMNUC PII KUUH (also from your list)
]

repetition_signs = [
    'ៗ' # LEK TOO [cite: 79]
]

currency_symbols = [
    '៛' # RIEL [cite: 79]
]

numbers = ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩']

en_numbers = ['0', '1','2','3','4','5','6','7','8','9']
en_sign = ['!','@','#','$','%','&','(',')','-','+','=','[',']','?',]

# --- 8. DEPRECATED CHARACTERS ---
# You should avoid using these to create new text. They are included in Unicode for backward compatibility. [cite: 106, 107]
deprecated_chars = [
    'ឣ', # DEPRECATED KHMER INDEPENDENT VOWEL QAQ (Use U+17A2 instead) [cite: 79]
    'ឤ', # DEPRECATED KHMER INDEPENDENT VOWEL QAA (Use U+17A2 U+17B6 instead) [cite: 79]
    '៓'  # KHMER SIGN BATHAMASAT (Use U+19E0 from the Khmer Symbols block instead) [cite: 79]
]

base_consonants = consonants_a_series + consonants_o_series + [consonant_no_subscript]
subscriptable_consonants = consonants_a_series + consonants_o_series
subscriptable_consonants_no_ro = [c for c in subscriptable_consonants if c != 'រ']

def generate_independent_vowel_clusters():
    """
    Generates syllables made of an independent vowel followed by a coeng.
    Example: ឱ្យ
    """
    base = random.choice(independent_vowels)
    coeng = random.choice(subscriptable_consonants)
    return base + COENG + coeng


def generate_standalone_symbols():
    """
    Randomly selects from numbers, punctuation, and other symbols.
    """
    all_symbols = numbers + punctuations + repetition_signs + currency_symbols + en_numbers + en_sign
    return random.choice(all_symbols)

# -*- coding: utf-8 -*-
import random

def generate_random_syllables():
    """
    Randomly generates a specified number of valid Khmer syllables,
    following all canonical ordering and compatibility rules.
    """

    # 1. Start with a Base Consonant
    base = random.choice(base_consonants)
    syllable = base

    # 2. Add Robat? (less likely)
    if random.random() < 0.05: # 5% chance
        syllable += robat
        return syllable

    # 3. Add Coengs?
    num_coengs = random.choices([0, 1, 2], weights=[80, 15, 5], k=1)[0]
    if num_coengs == 1:
        syllable += COENG + random.choice(subscriptable_consonants)
    elif num_coengs == 2:
        # Special rule for Ro (រ): must be encoded last
        coeng1 = random.choice(subscriptable_consonants_no_ro)
        coeng2 = random.choice(subscriptable_consonants)
        syllable += COENG + coeng1 + COENG + coeng2
    
    # 4. Add Shifter?
    # Only add a shifter if no vowel has been added yet, and it's compatible
    if random.random() < 0.05: # 20% chance
        if base in consonants_a_series:
            syllable += shifters['a_to_o']
        elif base in consonants_o_series:
            syllable += shifters['o_to_a']
    
    # 5. Add Vowel?
    if random.random() < 0.85: # 85% chance of having a vowel
            syllable += random.choice(dependent_vowels)

    # 6. Add Modifiers?
    num_modifiers = random.choices([0, 1, 2], weights=[85, 10, 5], k=1)[0]
    for _ in range(num_modifiers):
        syllable += random.choice(modifiers)

    # 7. Add Final? (less likely)
    if random.random() < 0.05: # 10% chance
        syllable += random.choice(final_signs)
    
    return syllable


def get_rand_khmer_syllable():
    rand_choices = random.choices([0, 1, 2], weights=[80, 10, 10], k=1)[0]
    if rand_choices == 0:
        return generate_random_syllables()
    elif rand_choices == 1:
        return generate_independent_vowel_clusters()
    
    return generate_standalone_symbols()
