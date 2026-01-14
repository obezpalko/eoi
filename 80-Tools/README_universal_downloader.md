# Universal Image Downloader

A flexible Python tool for downloading images using DuckDuckGo image search with support for multiple input formats.

## Features

- ✅ **DuckDuckGo Image Search** - Uses DDG for reliable image results
- ✅ **Multiple Input Formats** - CSV, JSON, Markdown, or command-line
- ✅ **Skip Existing Images** - Only downloads missing files
- ✅ **Configurable** - Image size, quality, delays, etc.
- ✅ **Auto-resize** - Automatically resizes images to specified dimensions
- ✅ **Rate Limiting** - Configurable delays to avoid being blocked

## Installation

```bash
# Install required dependencies
pip install duckduckgo-search pillow requests
```

## Usage

### 1. From CSV File

Create a CSV file with `filename` and `query` columns:

```csv
filename,query
red_car,red sports car
blue_house,blue house with garden
```

Then run:

```bash
python3 download_images_universal.py --csv images.csv --output ./images
```

### 2. From JSON File

Create a JSON file with an array of objects:

```json
[
  {"filename": "red_car", "query": "red sports car"},
  {"filename": "blue_house", "query": "blue house with garden"}
]
```

Then run:

```bash
python3 download_images_universal.py --json images.json --output ./images
```

### 3. From Markdown File

If you have a markdown file with image links like:

```markdown
| **el coche** | Vehicle | ![[../60-Cultura/España vs Hispanoamerica/coche.jpg]] |
| **la casa** | House | ![[images/casa.jpg]] |
```

The tool will automatically extract filenames and search terms:

```bash
python3 download_images_universal.py --md vocabulary.md --output ./images
```

### 4. From Command Line

Specify items directly as `filename:query` pairs:

```bash
python3 download_images_universal.py \
  --output ./images \
  --items "red_car:red sports car" "blue_house:blue house"
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output`, `-o` | Output directory for images | Required |
| `--size` | Max image size (e.g., 512x512, 256x256) | 512x512 |
| `--quality` | JPEG quality (1-100) | 85 |
| `--delay` | Delay between downloads (seconds) | 1.0 |
| `--max-results` | Max search results to try per image | 5 |
| `--force` | Re-download existing images | false |
| `--extension` | Output file extension (jpg/jpeg/png) | jpg |

## Examples

### Download with custom size

```bash
python3 download_images_universal.py \
  --csv images.csv \
  --output ./images \
  --size 256x256
```

### Download with longer delay (avoid rate limiting)

```bash
python3 download_images_universal.py \
  --csv images.csv \
  --output ./images \
  --delay 2.0
```

### Force re-download existing images

```bash
python3 download_images_universal.py \
  --csv images.csv \
  --output ./images \
  --force
```

### Download as PNG instead of JPEG

```bash
python3 download_images_universal.py \
  --csv images.csv \
  --output ./images \
  --extension png
```

## Example Files

Example input files are provided in the `examples/` directory:

- `examples/images.csv` - CSV format example
- `examples/images.json` - JSON format example

## How It Works

1. **Load Items** - Reads image filenames and search queries from your specified source
2. **Check Existing** - Skips files that already exist (unless `--force` is used)
3. **Search DDG** - Searches DuckDuckGo for images matching the query
4. **Download & Resize** - Downloads images and resizes them to specified dimensions
5. **Save** - Saves images as JPEG (or PNG) with the specified filename

## Comparison with Old Scripts

This universal downloader replaces the following specialized scripts:

- ❌ `download_color_images.py` - Hardcoded for colors
- ❌ `download_profesiones_ddg.py` - Hardcoded for professions  
- ❌ `download_missing_profesiones.py` - Hardcoded dictionary
- ❌ `download_navidad_images.py` - Hardcoded for Christmas

✅ Use `download_images_universal.py` for all image download tasks!

## Tips

1. **Be specific in search queries** - "red sports car" works better than just "car"
2. **Use delays** - Increase `--delay` if you're downloading many images
3. **Check results** - Review downloaded images and adjust queries if needed
4. **Markdown parsing** - Works best with table format in markdown files

## Troubleshooting

### No images found
- Try making your search query more specific
- Check that DuckDuckGo returns results for your query in a browser
- Try different search terms

### Download errors
- Check your internet connection
- Increase `--delay` to avoid rate limiting
- Some image URLs may be invalid or blocked

### Import errors
```bash
# Make sure dependencies are installed
pip install duckduckgo-search pillow requests
```

