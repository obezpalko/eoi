# Migration Guide: Old Scripts → Universal Downloader

This guide shows how to migrate from the old specialized downloaders to the new universal downloader.

## Summary of Changes

**OLD:** Multiple specialized scripts with hardcoded data
- `download_color_images.py` - Hardcoded for colors
- `download_profesiones_ddg.py` - Hardcoded table parsing
- `download_missing_profesiones.py` - Hardcoded dictionary
- `download_navidad_images.py` - Hardcoded dictionary
- `download_images.py` - Mixed Wikimedia/Flickr with hardcoded mappings

**NEW:** Single universal script with flexible input
- `download_images_universal.py` - Works with CSV, JSON, Markdown, or command-line

## Migration Examples

### Example 1: Profesiones (from hardcoded script)

**OLD:**
```bash
python3 download_profesiones_ddg.py \
  --md "30-Vocabulario/Temas/Profesiones/Profesiones.md" \
  --output "30-Vocabulario/Temas/Profesiones"
```

**NEW:**
```bash
python3 download_images_universal.py \
  --md "30-Vocabulario/Temas/Profesiones/Profesiones.md" \
  --output "30-Vocabulario/Temas/Profesiones" \
  --size 512x512
```

### Example 2: Missing Images (from hardcoded dictionary)

**OLD:**
```python
# download_missing_profesiones.py
MISSING_IMAGES = {
    'dependiente': 'dependiente tienda vendedor trabajando',
    'empresario': 'empresario hombre negocios traje',
    'fotografo': 'fotógrafo cámara profesional',
}
```

**NEW (create CSV):**
```csv
filename,query
dependiente,dependiente tienda vendedor trabajando
empresario,empresario hombre negocios traje
fotografo,fotógrafo cámara profesional
```

```bash
python3 download_images_universal.py \
  --csv missing_profesiones.csv \
  --output "30-Vocabulario/Temas/Profesiones"
```

### Example 3: Navidad (from hardcoded dictionary)

**OLD:**
```python
# download_navidad_images.py
IMAGES = {
    "reyes_magos.jpg": "Reyes Magos Melchor Gaspar Baltasar",
    "cabalgata.jpg": "cabalgata reyes magos parade spain",
    "roscon_de_reyes.jpg": "roscon de reyes cake spain",
}
```

**NEW (use JSON):**
```json
[
  {"filename": "reyes_magos", "query": "Reyes Magos Melchor Gaspar Baltasar"},
  {"filename": "cabalgata", "query": "cabalgata reyes magos parade spain"},
  {"filename": "roscon_de_reyes", "query": "roscon de reyes cake spain"}
]
```

```bash
python3 download_images_universal.py \
  --json navidad_images.json \
  --output "30-Vocabulario/Temas/Navidad en España" \
  --size 500x400
```

### Example 4: Quick Command Line

**OLD:** Had to edit Python file and run

**NEW:** Direct command line
```bash
python3 download_images_universal.py \
  --output ./images \
  --items \
    "gato:gato negro" \
    "perro:perro blanco" \
    "casa:casa azul"
```

## Creating Input Files

### From Existing Dictionaries

If you have a Python dictionary in an old script:

```python
WORDS = {
    "palabra1": "search query 1",
    "palabra2": "search query 2",
}
```

Convert to CSV:
```bash
echo "filename,query" > output.csv
# Then add each entry manually or with a script
```

Or convert to JSON:
```bash
python3 -c "
import json
words = {
    'palabra1': 'search query 1',
    'palabra2': 'search query 2',
}
data = [{'filename': k, 'query': v} for k, v in words.items()]
print(json.dumps(data, indent=2, ensure_ascii=False))
" > output.json
```

### From Markdown Files

If your markdown has image links like `![[path/file.jpg]]`, the universal downloader can extract them automatically:

```bash
python3 download_images_universal.py \
  --md "your-file.md" \
  --output "./images"
```

## Benefits of Universal Downloader

✅ **No hardcoding** - All data comes from input files or parameters
✅ **Reusable** - One script for all vocabulary topics
✅ **Flexible** - Multiple input formats (CSV, JSON, MD, CLI)
✅ **Configurable** - Size, quality, delays, etc. all adjustable
✅ **Skip existing** - Only downloads missing images
✅ **Better error handling** - Tries multiple images per query

## Recommended Workflow

1. **For new vocabulary topics:**
   - Create a CSV or JSON file with your words and search queries
   - Run the universal downloader
   - Review results and adjust queries if needed

2. **For existing markdown files with image links:**
   - Use `--md` parameter to auto-extract
   - Script will parse table format if available

3. **For quick one-off downloads:**
   - Use `--items` for direct command-line input
   - Perfect for 1-5 images

## Common Options

```bash
# Standard download
python3 download_images_universal.py --csv words.csv --output ./images

# Larger images
python3 download_images_universal.py --csv words.csv --output ./images --size 1024x1024

# Slower download (avoid rate limiting)
python3 download_images_universal.py --csv words.csv --output ./images --delay 2.0

# Re-download existing images
python3 download_images_universal.py --csv words.csv --output ./images --force

# Lower quality for smaller files
python3 download_images_universal.py --csv words.csv --output ./images --quality 70
```

## Converting Old Scripts

If you want to convert an old script:

1. Identify the hardcoded dictionary/data
2. Export to CSV or JSON format
3. Replace script call with universal downloader call
4. Test with a few images first
5. Run full batch

## Tips

- Start with small batches to test queries
- Use specific search terms for better results
- Adjust `--delay` if getting rate limited
- Check downloaded images and refine queries as needed
- Keep your CSV/JSON files for future re-downloads

