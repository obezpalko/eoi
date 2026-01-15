#!/bin/bash
# Re-download square images with proper aspect ratio preservation
# Max size: 256x256 but maintains aspect ratio

cd "$(dirname "$0")/.."

echo "Re-downloading images with proper aspect ratio (max 256x256)..."
echo "This will take approximately 3-5 minutes"
echo ""

# Colores ejemplos (37 images)
echo "=== 1/5: Colores ejemplos (37 images) ==="
python3 80-Tools/download_images_universal.py \
  --csv 80-Tools/redownload_ejemplos.csv \
  --output 30-Vocabulario/Temas/Colores/ejemplos \
  --size 256x256 \
  --quality 85 \
  --delay 1.5 \
  --force

echo ""
echo "=== 2/5: Ropa y Accesorios (26 images) ==="
python3 80-Tools/download_images_universal.py \
  --csv "80-Tools/redownload_Ropa y Accesorios.csv" \
  --output "30-Vocabulario/Temas/Ropa y Accesorios" \
  --size 256x256 \
  --quality 85 \
  --delay 1.5 \
  --force

echo ""
echo "=== 3/5: Siempre Plural (9 images) ==="
python3 80-Tools/download_images_universal.py \
  --csv "80-Tools/redownload_Siempre Plural.csv" \
  --output "30-Vocabulario/Temas/Siempre Plural" \
  --size 256x256 \
  --quality 85 \
  --delay 1.5 \
  --force

echo ""
echo "=== 4/5: Siempre Singular (8 images) ==="
python3 80-Tools/download_images_universal.py \
  --csv "80-Tools/redownload_Siempre Singular.csv" \
  --output "30-Vocabulario/Temas/Siempre Singular" \
  --size 256x256 \
  --quality 85 \
  --delay 1.5 \
  --force

echo ""
echo "=== 5/5: España vs Hispanoamerica (5 images) ==="
python3 80-Tools/download_images_universal.py \
  --csv "80-Tools/redownload_España vs Hispanoamerica.csv" \
  --output "60-Cultura/España vs Hispanoamerica" \
  --size 256x256 \
  --quality 85 \
  --delay 1.5 \
  --force

echo ""
echo "============================================"
echo "✓ Complete! All images re-downloaded with proper aspect ratio"
echo "============================================"
