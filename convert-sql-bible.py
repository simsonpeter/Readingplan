#!/usr/bin/env python3
"""
Convert SQL dump Bible file to JSON format compatible with Readingplan app.
Handles SQL INSERT statements from Bible databases.
"""

import json
import sys
import os
import re

# Tamil book names in Romanized form
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

def parse_sql_inserts(sql_content):
    """Parse SQL INSERT statements and extract verse data."""
    verses = []
    
    # Pattern to match INSERT statements
    # Handles various formats:
    # INSERT INTO table VALUES (1, 2, 3, 'text');
    # INSERT INTO table (col1, col2, col3, col4) VALUES (1, 2, 3, 'text');
    insert_pattern = re.compile(
        r'INSERT\s+INTO\s+\w+\s*(?:\([^)]+\))?\s*VALUES\s*\(([^)]+)\)',
        re.IGNORECASE | re.MULTILINE
    )
    
    # Also handle multi-line INSERTs
    # Remove comments and clean up
    sql_content = re.sub(r'--.*?$', '', sql_content, flags=re.MULTILINE)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    
    matches = insert_pattern.findall(sql_content)
    
    for match in matches:
        # Parse values - handle quoted strings and numbers
        values = []
        current_value = ""
        in_quotes = False
        quote_char = None
        
        for char in match:
            if not in_quotes:
                if char in ("'", '"'):
                    in_quotes = True
                    quote_char = char
                    current_value = ""
                elif char == ',':
                    if current_value.strip():
                        # Try to convert to number
                        val = current_value.strip()
                        try:
                            if '.' in val:
                                values.append(float(val))
                            else:
                                values.append(int(val))
                        except:
                            values.append(val)
                    current_value = ""
                elif char not in (' ', '\n', '\t'):
                    current_value += char
            else:
                if char == quote_char and (not current_value or current_value[-1] != '\\'):
                    # End of quoted string
                    values.append(current_value)
                    current_value = ""
                    in_quotes = False
                    quote_char = None
                else:
                    current_value += char
        
        # Add last value
        if current_value.strip() or in_quotes:
            if in_quotes:
                values.append(current_value)
            else:
                val = current_value.strip()
                try:
                    if '.' in val:
                        values.append(float(val))
                    else:
                        values.append(int(val))
                except:
                    values.append(val)
        
        # Expecting: book, chapter, verse, text (or similar order)
        if len(values) >= 4:
            # Try different column orders
            # Common: book, chapter, verse, text
            book_num = values[0]
            chapter_num = values[1]
            verse_num = values[2]
            verse_text = values[3]
            
            verses.append((book_num, chapter_num, verse_num, verse_text))
    
    return verses

def convert_sql_to_json(sql_path, output_path, book_names=None):
    """Convert SQL dump file to JSON format."""
    print(f"Reading SQL file: {sql_path}")
    
    with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
        sql_content = f.read()
    
    print("Parsing SQL INSERT statements...")
    verses = parse_sql_inserts(sql_content)
    
    if not verses:
        print("ERROR: No INSERT statements found or could not parse SQL file.")
        print("Trying alternative parsing method...")
        
        # Alternative: look for table structure and data patterns
        # Try to find CREATE TABLE to understand structure
        create_match = re.search(r'CREATE\s+TABLE\s+(\w+)\s*\(([^)]+)\)', sql_content, re.IGNORECASE)
        if create_match:
            table_name = create_match.group(1)
            columns = [col.strip().split()[0] for col in create_match.group(2).split(',')]
            print(f"Found table: {table_name}")
            print(f"Columns: {columns}")
        
        # Try simpler pattern: lines with numbers and text
        lines = sql_content.split('\n')
        for line in lines:
            # Look for patterns like: (1, 2, 3, 'text')
            pattern = r'\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*[\'"]([^\'"]+)[\'"]\)'
            matches = re.findall(pattern, line)
            for match in matches:
                verses.append((int(match[0]), int(match[1]), int(match[2]), match[3]))
    
    if not verses:
        print("ERROR: Could not extract verse data from SQL file.")
        return False
    
    print(f"Found {len(verses)} verses")
    
    # Organize into JSON structure (same as SQLite converter)
    books = {}
    
    for row in verses:
        book_num, chapter_num, verse_num, verse_text = row
        
        # Convert to integers if needed
        try:
            book_num = int(book_num) if isinstance(book_num, (int, str)) and str(book_num).isdigit() else book_num
            chapter_num = int(chapter_num) if isinstance(chapter_num, (int, str)) and str(chapter_num).isdigit() else chapter_num
            verse_num = int(verse_num) if isinstance(verse_num, (int, str)) and str(verse_num).isdigit() else verse_num
        except:
            pass
        
        # Handle book number encoding
        if isinstance(book_num, int):
            if book_num >= 10 and book_num % 10 == 0:
                book_idx = (book_num // 10) - 1
            elif book_num > 0 and book_num <= 66:
                book_idx = book_num - 1
            else:
                book_idx = book_num if book_num >= 0 else None
        else:
            book_idx = None
            if book_names:
                for i, name in enumerate(book_names):
                    if str(book_num).lower() == name.lower():
                        book_idx = i
                        break
        
        if book_idx is None:
            try:
                book_idx = int(book_num) - 1
            except:
                print(f"Warning: Could not determine book index for {book_num}")
                continue
        
        if book_idx < 0 or book_idx >= 66:
            continue
        
        if book_idx not in books:
            books[book_idx] = {}
        
        chapter_idx = int(chapter_num) - 1 if isinstance(chapter_num, (int, str)) and str(chapter_num).isdigit() else int(chapter_num)
        if chapter_idx not in books[book_idx]:
            books[book_idx][chapter_idx] = []
        
        verse_idx = int(verse_num) - 1 if isinstance(verse_num, (int, str)) and str(verse_num).isdigit() else int(verse_num)
        
        while len(books[book_idx][chapter_idx]) <= verse_idx:
            books[book_idx][chapter_idx].append("")
        
        books[book_idx][chapter_idx][verse_idx] = verse_text or ""
    
    # Convert to required JSON format
    json_books = []
    for book_idx in range(66):
        if book_idx not in books:
            json_books.append({"Chapter": []})
            continue
        
        chapters = []
        max_chapter = max(books[book_idx].keys()) if books[book_idx] else 0
        
        for chapter_idx in range(max_chapter + 1):
            if chapter_idx not in books[book_idx]:
                chapters.append({"Verse": []})
                continue
            
            verses = []
            max_verse = len(books[book_idx][chapter_idx]) - 1
            
            for verse_idx in range(max_verse + 1):
                verse_text = books[book_idx][chapter_idx][verse_idx] if verse_idx < len(books[book_idx][chapter_idx]) else ""
                if verse_text:
                    verses.append({
                        "Verseid": f"{book_idx:02d}{chapter_idx:03d}{verse_idx:03d}",
                        "Verse": verse_text
                    })
            
            chapters.append({"Verse": verses})
        
        json_books.append({"Chapter": chapters})
    
    output_data = {"Book": json_books}
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent='\t')
    
    print(f"\n✅ Successfully converted to {output_path}")
    print(f"   Books: {len(json_books)}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert-sql-bible.py <sql_file> [output_file]")
        print("\nExample:")
        print("  python3 convert-sql-bible.py bibles/TRB.sql bibles/tamilromanizedbible.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.sql', '.json')
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        print(f"\nPlease ensure the file exists. Searching for TRB files...")
        # Try to find it
        import subprocess
        result = subprocess.run(['find', os.path.dirname(input_file) or '.', '-name', '*TRB*', '-o', '-name', '*.sql'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"Found files: {result.stdout}")
        sys.exit(1)
    
    print(f"Converting {input_file} to {output_file}...")
    success = convert_sql_to_json(input_file, output_file, TAMIL_ROMANIZED_BOOK_NAMES)
    
    if not success:
        sys.exit(1)

