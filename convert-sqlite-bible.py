#!/usr/bin/env python3
"""
Convert SQLite Bible database to JSON format compatible with Readingplan app.
Supports Tamil Romanized Bible and other Bible translations in SQLite format.
"""

import sqlite3
import json
import sys
import os

# Tamil book names in Romanized form (you may need to adjust these)
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

def detect_sqlite_structure(db_path):
    """Detect the structure of the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found tables: {tables}")
    
    # Try to detect common Bible database structures
    structure = {}
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        structure[table] = columns
        print(f"  {table}: {columns}")
        
        # Sample a few rows
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        if rows:
            print(f"    Sample rows: {len(rows)}")
    
    conn.close()
    return structure, tables

def convert_sqlite_to_json(db_path, output_path, book_names=None):
    """
    Convert SQLite Bible database to JSON format.
    
    Expected SQLite structure (one of these):
    1. Table: verses (book, chapter, verse, text)
    2. Table: bible (book_number, chapter, verse, text)
    3. Table: books, chapters, verses (normalized)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Detect structure
    structure, tables = detect_sqlite_structure(db_path)
    
    # Try to find the right table and columns
    verse_table = None
    book_col = None
    chapter_col = None
    verse_col = None
    text_col = None
    
    # Common patterns
    for table in tables:
        cols = structure[table]
        cols_lower = [c.lower() for c in cols]
        
        # Check for common column names
        if any('verse' in c.lower() or 'text' in c.lower() or 'content' in c.lower() for c in cols):
            verse_table = table
            
            # Find book column
            for c in cols:
                c_lower = c.lower()
                if 'book' in c_lower and book_col is None:
                    book_col = c
                elif ('chapter' in c_lower or 'chap' in c_lower) and chapter_col is None:
                    chapter_col = c
                elif 'verse' in c_lower and verse_col is None:
                    verse_col = c
                elif ('text' in c_lower or 'content' in c_lower or 'verse_text' in c_lower) and text_col is None:
                    text_col = c
            
            if book_col and chapter_col and verse_col and text_col:
                break
    
    if not verse_table:
        # Try to query all tables to find the right one
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table} LIMIT 1")
                row = cursor.fetchone()
                if row and len(row) >= 4:
                    verse_table = table
                    # Assume standard order: book, chapter, verse, text
                    cols = structure[table]
                    if len(cols) >= 4:
                        book_col = cols[0]
                        chapter_col = cols[1]
                        verse_col = cols[2]
                        text_col = cols[3]
                        break
            except:
                continue
    
    if not verse_table:
        print("ERROR: Could not detect Bible database structure.")
        print("Please ensure the database has a table with book, chapter, verse, and text columns.")
        conn.close()
        return False
    
    print(f"\nUsing table: {verse_table}")
    print(f"Columns: book={book_col}, chapter={chapter_col}, verse={verse_col}, text={text_col}")
    
    # Query all verses
    query = f"SELECT {book_col}, {chapter_col}, {verse_col}, {text_col} FROM {verse_table} ORDER BY {book_col}, {chapter_col}, {verse_col}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} verses")
    
    # Organize into JSON structure
    books = {}
    
    for row in rows:
        book_num, chapter_num, verse_num, verse_text = row
        
        # Convert to integers if needed
        try:
            book_num = int(book_num) if isinstance(book_num, (int, str)) and str(book_num).isdigit() else book_num
            chapter_num = int(chapter_num) if isinstance(chapter_num, (int, str)) and str(chapter_num).isdigit() else chapter_num
            verse_num = int(verse_num) if isinstance(verse_num, (int, str)) and str(verse_num).isdigit() else verse_num
        except:
            pass
        
        # Handle book number encoding (could be 1-66, or encoded like 10, 20, 30, etc.)
        if isinstance(book_num, int):
            # Check if it's encoded (e.g., 10, 20, 30 for books 1, 2, 3)
            if book_num >= 10 and book_num % 10 == 0:
                # Encoded format: divide by 10 and subtract 1 for 0-indexing
                book_idx = (book_num // 10) - 1
            elif book_num > 0 and book_num <= 66:
                # Standard 1-indexed format
                book_idx = book_num - 1
            else:
                # Try to use as-is (0-indexed)
                book_idx = book_num if book_num >= 0 else None
        else:
            # Try to find book by name
            book_idx = None
            if book_names:
                for i, name in enumerate(book_names):
                    if str(book_num).lower() == name.lower():
                        book_idx = i
                        break
        
        if book_idx is None:
            try:
                # Last resort: try to convert and assume 1-indexed
                book_idx = int(book_num) - 1
            except:
                print(f"Warning: Could not determine book index for {book_num}")
                continue
        
        # Ensure valid range
        if book_idx < 0 or book_idx >= 66:
            continue
        
        # Initialize book if needed
        if book_idx not in books:
            books[book_idx] = {}
        
        # Initialize chapter if needed
        chapter_idx = int(chapter_num) - 1 if isinstance(chapter_num, (int, str)) and str(chapter_num).isdigit() else int(chapter_num)
        if chapter_idx not in books[book_idx]:
            books[book_idx][chapter_idx] = []
        
        # Add verse
        verse_idx = int(verse_num) - 1 if isinstance(verse_num, (int, str)) and str(verse_num).isdigit() else int(verse_num)
        
        # Ensure verse array is large enough
        while len(books[book_idx][chapter_idx]) <= verse_idx:
            books[book_idx][chapter_idx].append("")
        
        books[book_idx][chapter_idx][verse_idx] = verse_text or ""
    
    # Convert to required JSON format
    json_books = []
    for book_idx in range(66):
        if book_idx not in books:
            # Empty book
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
                if verse_text:  # Only add non-empty verses
                    verses.append({
                        "Verseid": f"{book_idx:02d}{chapter_idx:03d}{verse_idx:03d}",
                        "Verse": verse_text
                    })
            
            chapters.append({"Verse": verses})
        
        json_books.append({"Chapter": chapters})
    
    # Create final JSON structure
    output_data = {"Book": json_books}
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent='\t')
    
    print(f"\n✅ Successfully converted to {output_path}")
    print(f"   Books: {len(json_books)}")
    
    conn.close()
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert-sqlite-bible.py <sqlite_file> [output_file]")
        print("\nExample:")
        print("  python3 convert-sqlite-bible.py bibles/tamil-romanized.sqlite3 bibles/tamilromanizedbible.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.sqlite3', '.json').replace('.db', '.json').replace('.sqlite', '.json')
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    print(f"Converting {input_file} to {output_file}...")
    success = convert_sqlite_to_json(input_file, output_file, TAMIL_ROMANIZED_BOOK_NAMES)
    
    if not success:
        sys.exit(1)

