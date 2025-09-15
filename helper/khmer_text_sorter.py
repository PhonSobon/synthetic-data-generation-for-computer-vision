"""
Note: 

Base Characters: 
    - Consonants (U+1780 - U+17A2)
    - Independent Vowel (U+17A5 - U+17B3)
Coeng: 
    -  KHMER SIGN COENG (U+17D2) + Base Characters (exclude LA (U+17A1) and Independent Vowel)
Dependent Vowels:
    -  Dependent Vowels (U+17B6-U+17C5)
Consonant Shifers:
    - KHMER SIGN MUUSIKATOAN (U+17C9) 
    - KHMER SIGN TRIISAP (U+17CA)
Diacritic & Modifier:
    - Diacritic & Modifier (U+17C6, U+17CB-U+17D1)
Finals and Punctuation:
    - KHMER SIGN REAHMUK (U+17C7)
    - KHMER SIGN YUUKALEAPIN TU (U+17C8)
    - Punctuation and Other (U+17D4-U+17DB)
Number:
    - KHMER NUMBER (U+17E0-U+17E9)

Syllable = Base Robat? Coengs? Shifer? Vowel? Modifers? Final? 

A detailed breakdown of the components is as follows: 
●  Base: This is the only mandatory component of a syllable. It must be a single character 
from the Base class, which includes all consonants (U+1780-U+17A2) and independent 
vowels (U+17A5-U+17B3). 
●  Robat?: An optional KHMER SIGN ROBAT (U+17CC). If present, it must immediately 
follow the Base. 
●  Coengs?: An optional sequence of one or two subscript consonants. Each subscript is 
encoded as a KHMER SIGN COENG (U+17D2) followed by a Base character. 
●  Shifer?: An optional consonant shifer, either KHMER SIGN MUUSIKATOAN (U+17C9) or 
KHMER SIGN TRIISAP (U+17CA). It must follow the entire consonant group (Base + 
Coengs). 
●  Vowel?: An optional dependent vowel (U+17B6-U+17C5). This includes single-codepoint 
representations of two-part vowels. 
●  Modifers?: An optional sequence of up to two non-spacing modifying signs, such as 
NIKAHIT (U+17C6) or BANTOC (U+17CB). 
●  Final?: An optional spacing fnal sign, either REAHMUK (U+17C7) or YUUKALEAPINTU 
(U+17C8).

Rule 1: The Base Character is Always First 
Rule 2: Robat (U+17CC) Follows the Base Immediately 
Rule 3: Subscript Consonants (Coengs) are Encoded Sequentially
    In Modern Khmer, a syllable can have up to two initial coengs (forming a three-consonant cluster).
    In such cases, the Coeng sequences are encoded in the order they appear visually, from top to botom. For 
    example, a cluster with a base, a frst subscript, and a second subscript would be encoded: 
    Base + Coeng1_Sequence + Coeng2_Sequence.
    Special Sub-Rule for Subscript Ro (រ) its Coeng sequence (U+17D2 U+179A) 
    must always be encoded second, as the fnal part of the consonant cluster, regardless 
    of its visual or phonetic position
Rule 4: Consonant Shifers Follow the Complete Consonant Cluster
Rule 5: Dependent Vowels Follow the Shifer
Rule 6: Modifying Signs and Finals are Encoded Last 

"""

def is_consonant(code: int) -> bool:
    if 0x1780 <= code <= 0x17A2:
        return True
    return False


def is_indp_vowel(code: int) -> bool:
    if 0x17A5 <= code <= 0x17B3:
        return True
    return False


def is_vowel(code: int) -> bool:
    if 0x17B6 <= code <= 0x17C5:
        return True
    return False


def is_diacritic(code: int) -> bool:
    if code == 0x17C6 or code == 0x17CB or 0x17CD <= code <= 0x17D1:
        return True
    return False


def is_final(code: int) -> bool:
    if 0x17C7 <= code <= 0x17C8:
        return True
    return False


def is_shifter(code: int) -> bool:
    if 0x17C9 == code or code == 0x17CA:
        return True
    return False


def is_robat(code: int) -> bool:
    if code == 0x17CC:
        return True
    return False


def is_coeng(code: int) -> bool:
    if code == 0x17D2:
        return True
    return False


def is_punctuation(code: int) -> bool:
    if 0x17D4 <= code <= 0x17DB:
        return True
    return False


def is_numberical(code: int) -> bool:
    if 0x17E0 <= code <= 0x17E9:
        return True
    return False


def is_standalone(code: int) -> bool:
    if  is_consonant(code) or \
        is_indp_vowel(code) or \
        is_numberical(code) or \
        is_punctuation(code):
        return True
    return False


def is_punctuation_or_final(code: int) -> bool:
    if is_punctuation(code) or \
        is_final(code):
        return True
    return False


def is_RO(code: int) -> bool:
    if 0x179A == code:
        return True
    return False


def is_dependent_only(code: int) -> bool:
    """
    Helper function to check for characters that CANNOT stand alone.
    """
    if is_vowel(code) or \
       is_coeng(code) or \
       is_diacritic(code) or \
       is_robat(code) or \
       is_shifter(code) or \
       is_final(code):
        return True
    return False


def merge_temp_result(temp: list[str], result: str) -> str:
    for char in temp:
        if char != '':
            result += char
    return result


def sort_khm_word(text: str) -> str:
    """
    This function will sort khmer word according to Unicode.
    """

    result = ""

    # temp store 10 character with this order
    # Base + Robat + Coeng + Con + Coeng + Con + S + V + D + F
    # 0      1       2       3     4       5     6   7   8   9
    temp = [""] * 10
    i = 0
    text_length = len(text)
    
    while i < text_length:
        char = text[i]
        code = ord(char)

        if code == 0x200B:
            i += 1
            continue

        # This block handles characters that start a new syllable
        if is_standalone(code):
            # If a syllable was being built, merge it first.
            if temp[0] != '':
                result = merge_temp_result(temp, result)
                temp = [""] * 10
            
            # If it's a number or punctuation, just add it directly.
            # Otherwise, start a new syllable in the temp buffer.
            if is_numberical(code) or is_punctuation(code):
                result += char
            else: # Must be a Consonant or Independent Vowel
                temp[0] = char
            i += 1
            # print(temp)
        
        # This block handles characters that attach to the previous base character
        elif temp[0] != '':
            if is_robat(code) and temp[1] == '':
                temp[1] = char
            elif is_coeng(code) and i + 1 < text_length and temp[2] == '':
                next_char = text[i + 1]
                next_code = ord(next_char)
                if is_consonant(next_code) and not is_RO(next_code):
                    temp[2] = char
                    temp[3] = next_char
                    i += 1
                elif is_consonant(next_code) and is_RO(next_code):
                    temp[4] = char
                    temp[5] = next_char
                    i += 1
            elif is_coeng(code) and i + 1 < text_length and temp[4] == '':
                next_char = text[i + 1]
                next_code = ord(next_char)
                if is_consonant(next_code):
                    temp[4] = char
                    temp[5] = next_char
                    i += 1
            elif is_shifter(code) and temp[6] == '':
                temp[6] = char
            elif is_vowel(code) and temp[7] == '':
                temp[7] = char
            elif is_diacritic(code) and temp[8] == '':
                temp[8] = char
            elif is_final(code) and temp[9] == '':
                temp[9] = char

            # If the character doesn't fit the syllable rules,
            # end the current syllable and add the character.
            else:
                result = merge_temp_result(temp, result)
                temp = [""] * 10
                result += char
            i += 1
            # print(temp)

        # If a character is not Khmer (like space, newline, etc.)
        # or it's an attaching character with no base, treat it as a separator.
        else:
            i += 1
            # # Check if it's an invalid, orphaned dependent character.
            # if is_dependent_only(code):
            #     # If it is, we simply DISCARD it by moving to the next character.
            #     i += 1
            # # Otherwise, it's a legitimate separator (space, newline, etc.).
            # else:
            #     # We KEEP it by adding it to the result.
            #     result = merge_temp_result(temp, result) # Not really needed but safe
            #     temp = [""] * 10
            #     result += char
            #     i += 1

            
    # After the loop, merge any leftover characters in the temp buffer
    if temp[0] != '':
        result = merge_temp_result(temp, result)
    
    # print((result))
    return result


def merge_temp(temp: list[str]) -> str:
    result = ''
    for char in temp:
        if char != '':
            result += char
    return result


def sort_word2sub(text: str) -> list[str]:
    """
    This function will first sort the words according to Unicode
    Then it breaks down the word into subsyllable
    """
    result = []

    # temp store 10 character with this order
    # Base + Robat + Coeng + Con + Coeng + Con + S + V + D + F
    # 0      1       2       3     4       5     6   7   8   9
    temp = [""] * 10
    i = 0
    text_length = len(text)

    while i < text_length:
        char = text[i]
        code = ord(char)

        if code == 0x200B:
            i += 1
            continue

        # This block handles characters that start a new syllable
        if is_standalone(code):
            # If a syllable was being built, merge it first.
            if temp[0] != '':
                result.append(merge_temp(temp))
                temp = [""] * 10
            
            # If it's a number or punctuation, just add it directly.
            # Otherwise, start a new syllable in the temp buffer.
            if is_numberical(code) or is_punctuation(code):
                result.append(char)
            else: # Must be a Consonant or Independent Vowel
                temp[0] = char
            i += 1
            # print(temp)
        
        # This block handles characters that attach to the previous base character
        elif temp[0] != '':
            if is_robat(code) and temp[1] == '':
                temp[1] = char
            elif is_coeng(code) and i + 1 < text_length and temp[2] == '':
                next_char = text[i + 1]
                next_code = ord(next_char)
                if is_consonant(next_code) and not is_RO(next_code):
                    temp[2] = char
                    temp[3] = next_char
                    i += 1
                elif is_consonant(next_code) and is_RO(next_code):
                    temp[4] = char
                    temp[5] = next_char
                    i += 1
            elif is_coeng(code) and i + 1 < text_length and temp[4] == '':
                next_char = text[i + 1]
                next_code = ord(next_char)
                if is_consonant(next_code):
                    temp[4] = char
                    temp[5] = next_char
                    i += 1
            elif is_shifter(code) and temp[6] == '':
                temp[6] = char
            elif is_vowel(code) and temp[7] == '':
                temp[7] = char
            elif is_diacritic(code) and temp[8] == '':
                temp[8] = char
            elif is_final(code) and temp[9] == '':
                temp[9] = char

            # If the character doesn't fit the syllable rules,
            # end the current syllable and add the character.
            else:
                result.append(merge_temp(temp))
                temp = [""] * 10
                result.append(char)
            i += 1
            # print(temp)

        # If a character is not Khmer (like space, newline, etc.)
        # or it's an attaching character with no base, treat it as a separator.
        else:
            i += 1
            # # Check if it's an invalid, orphaned dependent character.
            # if is_dependent_only(code):
            #     # If it is, we simply DISCARD it by moving to the next character.
            #     i += 1
            # # Otherwise, it's a legitimate separator (space, newline, etc.).
            # else:
            #     # We KEEP it by adding it to the result.
            #     result.append(merge_temp(temp))
            #     temp = [""] * 10
            #     result.append(char)
            #     i += 1
            
    # After the loop, merge any leftover characters in the temp buffer
    if temp[0] != '':
        result.append(merge_temp(temp))
    
    # print((result))
    return result


def sort_text2sub(text: str) -> list[str]:
    new_text = []
    for word in text:
        new_text.extend(sort_word2sub(word))
    return new_text
