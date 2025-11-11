#!/usr/bin/env python3
"""
Convert Tamil Bible (JSON) to Romanized Tamil Bible using transliteration.
This script converts the complete Tamil Bible to Romanized format.
"""

import json
import sys
import os

# Basic Tamil to Roman transliteration mapping
# This is a simplified mapping - for better accuracy, consider using indic-transliteration library
TAMIL_TO_ROMAN = {
    # Vowels
    'அ': 'a', 'ஆ': 'aa', 'இ': 'i', 'ஈ': 'ii', 'உ': 'u', 'ஊ': 'uu',
    'எ': 'e', 'ஏ': 'ee', 'ஐ': 'ai', 'ஒ': 'o', 'ஓ': 'oo', 'ஔ': 'au',
    
    # Consonants
    'க': 'k', 'ங': 'ng', 'ச': 'ch', 'ஞ': 'nj', 'ட': 't', 'ண': 'n',
    'த': 'th', 'ந': 'n', 'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
    'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l', 'ற': 'r', 'ன': 'n',
    
    # Special characters
    'ஸ': 's', 'ஷ': 'sh', 'ஜ': 'j', 'ஹ': 'h', 'க்ஷ': 'ksh',
    
    # Common combinations
    'க்': 'k', 'ச்': 'ch', 'ட்': 't', 'த்': 'th', 'ப்': 'p',
}

# Extended mapping for common Tamil words and proper names
COMMON_WORDS = {
    'தேவன்': 'Devan', 'யேசு': 'Yesu', 'கிறிஸ்து': 'Christu',
    'பரலோகம்': 'Paralogam', 'பூமி': 'Bhoomi', 'வானம்': 'Vaanam',
}

def tamil_to_roman_simple(text):
    """
    Simple transliteration - this is a basic implementation.
    For better accuracy, you may want to use indic-transliteration library:
    pip install indic-transliteration
    """
    if not text:
        return text
    
    # Try common words first
    result = text
    for tamil, roman in COMMON_WORDS.items():
        result = result.replace(tamil, roman)
    
    # Basic character-by-character transliteration
    # Note: This is simplified and may not be perfect
    # For production use, consider indic-transliteration library
    output = []
    i = 0
    while i < len(result):
        char = result[i]
        if char in TAMIL_TO_ROMAN:
            output.append(TAMIL_TO_ROMAN[char])
        elif '\u0B80' <= char <= '\u0BFF':  # Tamil Unicode range
            # Tamil character not in mapping - keep as is or use library
            output.append(char)
        else:
            output.append(char)
        i += 1
    
    return ''.join(output)

def convert_bible_to_romanized(input_file, output_file):
    """Convert Tamil Bible JSON to Romanized format."""
    print(f"Reading Tamil Bible from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        tamil_bible = json.load(f)
    
    print(f"Found {len(tamil_bible.get('Book', []))} books")
    
    # Romanized book names
    TAMIL_ROMANIZED_BOOK_NAMES = [
        "Aadiyagam", "Yaathiraagam", "Leviyaragam", "Ennaagam", "Upagam", "Yosuva", 
        "Niyaayathipathikal", "Ruth", "1 Samuvel", "2 Samuvel", "1 Irajakkal", 
        "2 Irajakkal", "1 Nalagam", "2 Nalagam", "Esra", "Nekemiya", "Esther", "Yobu",
        "Sangeetham", "Neethimozhikal", "Pirasangi", "Unnathappattu", "Esaiya", 
        "Eremiya", "Pulambal", "Esekkiel", "Thaniyel", "Osiya", "Yovel", "Amos", 
        "Obadiya", "Yona", "Mika", "Nagum", "Abaguk", "Seppaniya", "Agai", 
        "Sakariya", "Malkiya", "Matteyu", "Marku", "Lukka", "Yovan", "Apostalar", 
        "Romer", "1 Korinthiyar", "2 Korinthiyar", "Kalathiyar", "Ephesiyar", 
        "Pilippiyar", "Koloseyar", "1 Thessaloniikeyar", "2 Thessaloniikeyar", 
        "1 Thimotheyu", "2 Thimotheyu", "Thittu", "Pilemon", "Epreyar", "Yakkobu", 
        "1 Peturu", "2 Peturu", "1 Yovan", "2 Yovan", "3 Yovan", "Yutha", "Veli"
    ]
    
    # Try to use indic-transliteration if available
    try:
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
        USE_LIBRARY = True
        print("✅ Using indic-transliteration library for accurate conversion")
    except ImportError:
        USE_LIBRARY = False
        print("⚠️  indic-transliteration not found. Using basic transliteration.")
        print("   For better accuracy, install: pip install indic-transliteration")
    
    romanized_books = []
    total_verses = 0
    
    for book_idx, book in enumerate(tamil_bible.get('Book', [])):
        if book_idx >= 66:
            break
        
        print(f"Processing book {book_idx + 1}/66...", end='\r')
        
        chapters = []
        for chapter in book.get('Chapter', []):
            verses = []
            for verse_obj in chapter.get('Verse', []):
                verse_text = verse_obj.get('Verse', '')
                
                if USE_LIBRARY:
                    try:
                        # Use indic-transliteration library
                        romanized_text = transliterate(verse_text, sanscript.TAMIL, sanscript.ITRANS)
                    except:
                        # Fallback to simple method
                        romanized_text = tamil_to_roman_simple(verse_text)
                else:
                    romanized_text = tamil_to_roman_simple(verse_text)
                
                verses.append({
                    "Verseid": verse_obj.get('Verseid', ''),
                    "Verse": romanized_text
                })
                total_verses += 1
            
            chapters.append({"Verse": verses})
        
        romanized_books.append({"Chapter": chapters})
    
    print(f"\n✅ Converted {total_verses} verses")
    
    # Create output structure
    output_data = {"Book": romanized_books}
    
    # Write to file
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent='\t')
    
    print(f"✅ Successfully created Romanized Bible: {output_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert-tamil-to-romanized.py [input_file] [output_file]")
        print("\nExample:")
        print("  python3 convert-tamil-to-romanized.py bibles/tamilbible.json bibles/tamilromanizedbible.json")
        sys.exit(1)
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'bibles/tamilbible.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'bibles/tamilromanizedbible.json'
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    success = convert_bible_to_romanized(input_file, output_file)
    
    if not success:
        sys.exit(1)

