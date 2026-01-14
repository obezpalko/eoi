# 80-Tools - Repository Management Tools

This directory contains various Python scripts and utilities for managing the EOI Spanish learning repository, particularly for downloading images, checking links, and maintaining file organization.

## 📋 Table of Contents

- [Installation](#installation)
- [Image Download Tools](#image-download-tools)
- [Image Management Tools](#image-management-tools)
- [Generation Tools](#generation-tools)
- [Legacy Tools](#legacy-tools)
- [Quick Reference](#quick-reference)

---

## 🔧 Installation

Most tools require Python 3 and the following dependencies:

```bash
pip install duckduckgo-search pillow requests
```

Some tools may require additional dependencies (check individual tool headers).

---

## 📥 Image Download Tools

### 1. `download_images_universal.py` ⭐ **RECOMMENDED**

**Universal image downloader** - The main tool for downloading images. Supports multiple input formats and is the recommended replacement for all specialized downloaders.

**Usage:**

```bash
# From CSV file
python3 download_images_universal.py --csv images.csv --output ./images

# From JSON file
python3 download_images_universal.py --json images.json --output ./images

# From Markdown file (auto-extracts image references)
python3 download_images_universal.py --md vocab.md --output ./images

# From command line
python3 download_images_universal.py --output ./images \
  --items "car:red car" "house:blue house"
```

**Options:**
- `--output, -o` - Output directory (required)
- `--size` - Max image size, e.g., `512x512` (default: `512x512`)
- `--quality` - JPEG quality 1-100 (default: `85`)
- `--delay` - Delay between downloads in seconds (default: `1.0`)
- `--max-results` - Max search results to try per image (default: `5`)
- `--force` - Re-download existing images
- `--extension` - Output extension: `jpg`, `jpeg`, or `png` (default: `jpg`)

**See also:** `README_universal_downloader.md` for detailed documentation.

---

### 2. `download_missing_images.py`

Helper script to automatically download missing images identified by `check_image_links.py`.

**Usage:**

```bash
python3 download_missing_images.py
```

The script will:
1. Scan all markdown files for broken image links
2. Group missing images by directory
3. Prompt you to download them using `download_images_universal.py`

---

## 🔍 Image Management Tools

### 3. `check_image_links.py`

**Check and fix broken image links** in all markdown files. Also identifies unused images.

**Usage:**

```bash
python3 check_image_links.py
```

**What it does:**
- Scans all `.md` files for image references (`![[image.jpg]]`)
- Checks if referenced images exist
- Attempts to fix broken links automatically
- Generates `unused_images.txt` with list of unused images

**Output:**
- Reports broken links with file locations
- Automatically fixes links where possible
- Creates `unused_images.txt` with unused images list

---

### 4. `fix_image_paths.py`

**Fix non-relative image paths** - Converts absolute paths like `![[60-Cultura/España vs Hispanoamerica/image.jpg]]` to relative paths like `![[image.jpg]]` when the file is already in that directory.

**Usage:**

```bash
python3 fix_image_paths.py
```

**What it does:**
- Finds image references using absolute paths (starting with directory names like `60-Cultura/`)
- Converts them to relative paths based on the markdown file's location
- Only modifies files if images can be found at the relative location

**Example:**
- Before: `![[60-Cultura/España vs Hispanoamerica/gafas.jpg]]`
- After: `![[gafas.jpg]]` (when file is in `60-Cultura/España vs Hispanoamerica/`)

---

## 🎨 Generation Tools

### 5. `generate_color_swatches.py`

Generates SVG color swatches for the color vocabulary section.

**Usage:**

```bash
python3 generate_color_swatches.py
```

**Output:** Creates SVG files in `30-Vocabulario/Temas/Colores/swatches/`

---

### 6. `generate_family_tree_svg.py`

Generates a family tree SVG diagram for the Spanish royal family, embedding images from the directory.

**Usage:**

```bash
python3 generate_family_tree_svg.py
```

**Output:** Creates `arbol_genealogico.svg` in `60-Cultura/Familia del rey/`

---

## 📚 Legacy Tools

The following tools are **deprecated** and should be replaced with `download_images_universal.py`. See `MIGRATION_GUIDE.md` for migration instructions.

### `download_color_images.py`
- **Replaced by:** `download_images_universal.py --md Colores.md`
- Downloads color example images from markdown file

### `download_profesiones_ddg.py`
- **Replaced by:** `download_images_universal.py --md Profesiones.md`
- Downloads profession images using DuckDuckGo

### `download_missing_profesiones.py`
- **Replaced by:** `download_images_universal.py` with CSV/JSON input
- Downloads missing profession images

### `download_navidad_images.py`
- **Replaced by:** `download_images_universal.py` with JSON input
- Downloads Christmas-related images

### `download_royal_family.py`
- Downloads images of Spanish royal family from Wikipedia
- Still functional but could be replaced with universal downloader

### `download_images.py`
- Mixed Wikimedia/Flickr downloader
- **Replaced by:** `download_images_universal.py`

---

## 📖 Quick Reference

### Common Workflows

#### Download images for a new vocabulary topic:

1. Create a CSV file with words and search queries:
   ```csv
   filename,query
   gato,gato negro
   perro,perro blanco
   ```

2. Run the downloader:
   ```bash
   python3 download_images_universal.py --csv words.csv \
     --output "30-Vocabulario/Temas/MiTema"
   ```

#### Fix image links after reorganizing files:

1. Check for broken links:
   ```bash
   python3 check_image_links.py
   ```

2. Fix non-relative paths:
   ```bash
   python3 fix_image_paths.py
   ```

3. Download any missing images:
   ```bash
   python3 download_missing_images.py
   ```

#### Extract and download images from existing markdown:

```bash
python3 download_images_universal.py \
  --md "30-Vocabulario/Temas/MiTema/MiTema.md" \
  --output "30-Vocabulario/Temas/MiTema"
```

---

## 📁 File Structure

```
80-Tools/
├── README.md                          # This file
├── README_universal_downloader.md     # Detailed universal downloader docs
├── QUICK_REFERENCE.md                 # Quick reference guide
├── MIGRATION_GUIDE.md                 # Guide for migrating from old tools
├── unused_images.txt                  # Generated list of unused images
│
├── download_images_universal.py       # ⭐ Main image downloader
├── check_image_links.py               # Check/fix image links
├── fix_image_paths.py                 # Fix non-relative paths
├── download_missing_images.py         # Download missing images
│
├── generate_color_swatches.py        # Generate color SVGs
├── generate_family_tree_svg.py        # Generate family tree SVG
│
├── examples/                          # Example input files
│   ├── images.csv
│   └── images.json
│
└── [legacy tools - see above]
```

---

## 🆘 Troubleshooting

### Images not downloading
- Check your internet connection
- Increase `--delay` to avoid rate limiting
- Try more specific search queries
- Check that DuckDuckGo returns results for your query

### Broken image links
- Run `check_image_links.py` to identify broken links
- Run `fix_image_paths.py` to fix non-relative paths
- Ensure images exist in the expected locations

### Import errors
```bash
pip install duckduckgo-search pillow requests
```

---

## 📝 Notes

- All tools use **relative paths** for portability
- Images are automatically resized to specified dimensions
- Tools skip existing images by default (use `--force` to re-download)
- The universal downloader is the recommended tool for all new image downloads

---

## 🔗 Related Documentation

- `README_universal_downloader.md` - Detailed universal downloader guide
- `QUICK_REFERENCE.md` - Quick command reference
- `MIGRATION_GUIDE.md` - Guide for migrating from legacy tools
- `../structure_recommendations.md` - Repository structure guidelines

---

**Last Updated:** 2025-01-19
