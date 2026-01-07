# Universal Image Downloader - Quick Reference

## Installation

```bash
pip install duckduckgo-search pillow requests
```

## Basic Usage

### From CSV File
```bash
python3 download_images_universal.py --csv images.csv --output ./images
```

### From JSON File
```bash
python3 download_images_universal.py --json images.json --output ./images
```

### From Markdown
```bash
python3 download_images_universal.py --md vocab.md --output ./images
```

### From Command Line
```bash
python3 download_images_universal.py --output ./images --items "car:red car" "house:blue house"
```

## CSV Format

```csv
filename,query
red_car,red sports car
blue_house,blue house with garden
```

## JSON Format

```json
[
  {"filename": "red_car", "query": "red sports car"},
  {"filename": "blue_house", "query": "blue house with garden"}
]
```

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--output`, `-o` | Output directory (required) | `--output ./images` |
| `--size` | Max image size | `--size 512x512` |
| `--quality` | JPEG quality (1-100) | `--quality 85` |
| `--delay` | Delay between downloads (sec) | `--delay 1.0` |
| `--max-results` | Max search results to try | `--max-results 5` |
| `--force` | Re-download existing images | `--force` |
| `--extension` | Output format (jpg/png) | `--extension png` |

## Quick Examples

**Standard download:**
```bash
python3 download_images_universal.py --csv words.csv --output ./vocab_images
```

**High quality, large images:**
```bash
python3 download_images_universal.py --csv words.csv --output ./images --size 1024x1024 --quality 95
```

**Slow download (avoid rate limits):**
```bash
python3 download_images_universal.py --csv words.csv --output ./images --delay 2.0
```

**Small thumbnails:**
```bash
python3 download_images_universal.py --csv words.csv --output ./thumbs --size 256x256 --quality 70
```

**Re-download everything:**
```bash
python3 download_images_universal.py --csv words.csv --output ./images --force
```

## Features

✅ DuckDuckGo image search
✅ Multiple input formats (CSV, JSON, Markdown, CLI)
✅ Skip existing images automatically
✅ Configurable size, quality, delays
✅ Auto-resize and format conversion
✅ Rate limiting protection
✅ Tries multiple images per query

## Input File Templates

Save these as templates for quick use:

**template.csv:**
```csv
filename,query
word1,search query for word1
word2,search query for word2
```

**template.json:**
```json
[
  {"filename": "word1", "query": "search query for word1"},
  {"filename": "word2", "query": "search query for word2"}
]
```

## Tips

1. **Be specific in queries** - "red sports car" > "car"
2. **Use delays** - Increase `--delay` if downloading many images
3. **Test first** - Try a few images before running large batches
4. **Check results** - Review downloaded images and adjust queries
5. **Keep input files** - Save CSV/JSON for future re-downloads

