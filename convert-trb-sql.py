#!/usr/bin/env python3
"""
Convert TRB.sql (tab-separated verse data) to JSON format compatible with Readingplan app.
"""

import json
import sys
import os

def convert_trb_to_json(sql_path, output_path):
    """Convert TRB.sql tab-separated file to JSON format."""
    print(f"Reading TRB.sql file: {sql_path}")
    
    books = {}
    verse_count = 0
    
    with open(sql_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where verse data starts (skip UPDATE statements)
    start_line = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('verse') and '\t' in line:
            # Check if it's the header or data
            parts = line.strip().split('\t')
            if len(parts) >= 5 and parts[1].isdigit():
                start_line = i
                break
            elif parts[0] == 'verse' and parts[1] == 'book':
                # Header line, data starts next
                start_line = i + 1
                break
    
    print(f"Verse data starts at line {start_line + 1}")
    
    # Process verse data
    for line_num, line in enumerate(lines[start_line:], start=start_line + 1):
        line = line.strip()
        if not line or not line.startswith('verse'):
            continue
        
        # Split by tab
        parts = line.split('\t')
        if len(parts) < 5:
            continue
        
        try:
            # Format: verse, book, chapter, verse, text
            book_num = int(parts[1])
            chapter_num = int(parts[2])
            verse_num = int(parts[3])
            verse_text = parts[4] if len(parts) > 4 else ' '.join(parts[4:])
            
            # Convert to 0-indexed
            book_idx = book_num - 1
            chapter_idx = chapter_num - 1
            verse_idx = verse_num - 1
            
            if book_idx < 0 or book_idx >= 66:
                continue
            
            # Initialize structures
            if book_idx not in books:
                books[book_idx] = {}
            if chapter_idx not in books[book_idx]:
                books[book_idx][chapter_idx] = []
            
            # Ensure verse array is large enough
            while len(books[book_idx][chapter_idx]) <= verse_idx:
                books[book_idx][chapter_idx].append("")
            
            books[book_idx][chapter_idx][verse_idx] = verse_text
            verse_count += 1
            
            if verse_count % 10000 == 0:
                print(f"  Processed {verse_count} verses...")
        
        except (ValueError, IndexError) as e:
            print(f"Warning: Skipping line {line_num}: {e}")
            continue
    
    print(f"Total verses processed: {verse_count}")
    
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
    
    # Count total verses in output
    total_verses = sum(len(chapter.get("Verse", [])) for book in json_books for chapter in book.get("Chapter", []))
    print(f"   Total verses: {total_verses}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert-trb-sql.py <trb_sql_file> [output_file]")
        print("\nExample:")
        print("  python3 convert-trb-sql.py bibles/TRB.sql bibles/tamilromanizedbible.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.sql', '.json')
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    print(f"Converting {input_file} to {output_file}...")
    success = convert_trb_to_json(input_file, output_file)
    
    if not success:
        sys.exit(1)

