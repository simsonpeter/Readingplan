#!/bin/bash
# Convert TAMOVR.SQLite3 (Tamil Red Letter Edition) to JSON format

cd "$(dirname "$0")"

# Check if file exists
if [ ! -f "bibles/TAMOVR.SQLite3" ]; then
    echo "❌ File not found: bibles/TAMOVR.SQLite3"
    echo "Please place TAMOVR.SQLite3 in the bibles/ directory"
    exit 1
fi

echo "🔄 Converting TAMOVR.SQLite3 to JSON format..."
python3 convert-sqlite-bible.py bibles/TAMOVR.SQLite3 bibles/tamilredletterbible.json

if [ $? -eq 0 ]; then
    echo "✅ Conversion successful!"
    echo "📦 Output: bibles/tamilredletterbible.json"
    echo ""
    echo "The Tamil Red Letter Bible has been added to the app."
    echo "It will appear in the language dropdown once the app is reloaded."
else
    echo "❌ Conversion failed"
    exit 1
fi

