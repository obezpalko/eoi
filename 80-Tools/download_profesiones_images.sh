#!/bin/bash
# Script to download profession images using DuckDuckGo (better quality than Wikimedia)
# This script is now COMPLETE - all 68 images have been downloaded!

cd /home/alexb/src/github.com/obezpalko/eoi

echo "Checking profession images..."
echo ""

TOTAL=$(ls -1 30-Vocabulario/Temas/Profesiones/*.jpg 2>/dev/null | wc -l)
EXPECTED=68

echo "Total images: $TOTAL"
echo "Expected: $EXPECTED"
echo ""

if [ "$TOTAL" -eq "$EXPECTED" ]; then
    echo "✓ All profession images are downloaded!"
    echo ""
    echo "Sample images:"
    ls -1 30-Vocabulario/Temas/Profesiones/*.jpg | head -10 | xargs -n 1 basename
else
    echo "⚠ Some images are missing. Downloading..."
    python3 80-Tools/download_missing_profesiones.py
fi

