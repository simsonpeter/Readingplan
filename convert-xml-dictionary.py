#!/usr/bin/env python3
"""
Convert XML dictionary (Sword format) to SQLite database
Supports Easton's Dictionary and similar XML formats
"""

import sqlite3
import xml.etree.ElementTree as ET
import sys
import os
import re

def parse_sword_xml(xml_file):
    """Parse XML dictionary format (Zefania, Sword, and other formats)"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    entries = []
    
    # Method 1: Zefania XML format (Easton Dictionary) - <item id="Word"> with <description> elements
    if root.tag == 'dictionary':
        for item in root.findall('.//item'):
            word = item.get('id') or ''
            if not word:
                continue
            
            # Collect all description elements
            descriptions = item.findall('description')
            if descriptions:
                # Combine all description texts
                definition_parts = []
                for desc in descriptions:
                    text = ''.join(desc.itertext()).strip()
                    if text:
                        definition_parts.append(text)
                definition = ' '.join(definition_parts).strip()
            else:
                # Fallback: get all text content excluding metadata elements
                text_parts = []
                for elem in item:
                    if elem.tag not in ['strong_id', 'title', 'transliteration', 'pronunciation', 'reflink', 'see']:
                        text = ''.join(elem.itertext()).strip()
                        if text:
                            text_parts.append(text)
                definition = ' '.join(text_parts).strip()
            
            if word and definition:
                entries.append((word.strip(), definition.strip()))
    
    # Method 2: Standard Sword format with <entry> tags
    if not entries:
        for entry in root.findall('.//entry'):
            # Get the word/topic
            word_elem = entry.find('key') or entry.find('word') or entry.find('title')
            if word_elem is None:
                # Try to get from attributes
                word = entry.get('key') or entry.get('word') or entry.get('title') or entry.get('name') or ''
            else:
                word = word_elem.text or ''
            
            # Get definition/content
            def_elem = entry.find('def') or entry.find('definition') or entry.find('content') or entry.find('body')
            if def_elem is None:
                # Get all text content, excluding the key/word element
                text_parts = []
                for elem in entry:
                    if elem.tag not in ['key', 'word', 'title', 'name']:
                        text_parts.append(''.join(elem.itertext()))
                definition = ' '.join(text_parts).strip()
                if not definition:
                    definition = ''.join(entry.itertext()).strip()
                    # Remove the word itself from definition if it appears at the start
                    if definition.startswith(word):
                        definition = definition[len(word):].strip()
            else:
                definition = ''.join(def_elem.itertext()).strip()
            
            if word and definition:
                entries.append((word.strip(), definition.strip()))
    
    # Method 3: Direct children as entries (alternative structure)
    if not entries:
        for child in root:
            if child.tag in ['entry', 'dictionaryEntry', 'dictEntry', 'item']:
                word = child.get('id') or child.get('key') or child.get('word') or child.get('title') or child.get('name') or ''
                definition = ''.join(child.itertext()).strip()
                if word and definition:
                    entries.append((word.strip(), definition.strip()))
            elif child.tag not in ['header', 'info', 'metadata', 'INFORMATION']:
                # Try to use tag name or first attribute as word
                word = child.tag if child.tag not in ['entry', 'dictionaryEntry', 'item'] else (child.get('id') or child.get('key') or child.get('word') or '')
                definition = ''.join(child.itertext()).strip()
                if word and definition and len(word) > 0:
                    entries.append((word.strip(), definition.strip()))
    
    return entries

def create_sqlite_db(entries, output_file):
    """Create SQLite database from dictionary entries"""
    # Remove existing database if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()
    
    # Create dictionary table
    cursor.execute('''
        CREATE TABLE dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            definition TEXT NOT NULL
        )
    ''')
    
    # Create words table for variations (optional, for future use)
    cursor.execute('''
        CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variation TEXT NOT NULL,
            standard_form TEXT NOT NULL
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('CREATE INDEX idx_topic ON dictionary(topic)')
    cursor.execute('CREATE INDEX idx_variation ON words(variation)')
    
    # Insert entries
    for word, definition in entries:
        cursor.execute('INSERT INTO dictionary (topic, definition) VALUES (?, ?)', 
                      (word, definition))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Created SQLite database: {output_file}")
    print(f"✅ Inserted {len(entries)} entries")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert-xml-dictionary.py <xml_file> [output_file]")
        print("Example: python3 convert-xml-dictionary.py dictionary/SF_2005-05-23_ENG_EASTON_(EASTON_DICTIONARY).xml dictionary/easton_dictionary.SQLite3")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else xml_file.replace('.xml', '.SQLite3')
    
    if not os.path.exists(xml_file):
        print(f"❌ Error: File not found: {xml_file}")
        sys.exit(1)
    
    print(f"📖 Parsing XML dictionary: {xml_file}")
    entries = parse_sword_xml(xml_file)
    
    if not entries:
        print("⚠️  No entries found. Trying alternative parsing...")
        # Try reading as plain text and parsing differently
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for common XML patterns
            # This is a fallback - adjust based on actual XML structure
            print("Please check the XML file structure and update the parser if needed.")
            sys.exit(1)
    
    print(f"📚 Found {len(entries)} dictionary entries")
    create_sqlite_db(entries, output_file)


