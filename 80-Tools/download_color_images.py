#!/usr/bin/env python3
"""
Download images for color examples from Colores.md using DuckDuckGo image search.
Resize images to 256x256 and save them locally.
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus
import requests
from PIL import Image
from io import BytesIO

def extract_examples_from_markdown(md_file):
    """Extract color names and example phrases from Colores.md."""
    examples = []
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all table rows with examples
    # New pattern: | **ColorName** | ![[swatches/...]] | ![[ejemplos/...]] | uso | _Example phrase._ |
    pattern = r'\|\s*\*\*([^*]+)\*\*\s*\|\s*!\[\[swatches/([^\]]+)\]\]\s*\|\s*!\[\[ejemplos/([^\]]+)\]\]\s*\|\s*([^|]+)\|\s*_([^_]+)_\s*\|'
    
    matches = re.findall(pattern, content)
    
    for match in matches:
        color_name = match[0].strip()
        swatch_file = match[1].strip()
        image_file = match[2].strip()
        uso = match[3].strip()
        example = match[4].strip()
        
        # Extract the key phrase from the example (remove formatting)
        # Example: "El coche es **rojo**." -> "coche rojo"
        clean_example = re.sub(r'\*\*([^*]+)\*\*', r'\1', example)
        clean_example = clean_example.replace('.', '').replace('_', '')
        
        # Extract noun and color for search
        search_term = clean_example.strip()
        
        examples.append({
            'color_name': color_name,
            'swatch_file': swatch_file,
            'uso': uso,
            'example': example,
            'search_term': search_term
        })
    
    return examples

def search_duckduckgo_images(query, max_results=3):
    """Search for images using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS
        
        print(f"  Searching DuckDuckGo for: {query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.images(
                keywords=query,
                max_results=max_results,
                safesearch='on',
                size='Medium'  # Medium size images are usually good quality
            ))
        
        if results:
            print(f"  Found {len(results)} images")
            return [r['image'] for r in results]
        else:
            print(f"  No images found")
            return []
        
    except Exception as e:
        print(f"  Error searching: {e}")
        return []

def download_and_resize_image(image_url, output_path, size=(256, 256)):
    """Download image from URL and resize to specified dimensions."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(image_url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Open image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize with high-quality resampling
        img_resized = img.resize(size, Image.Resampling.LANCZOS)
        
        # Save as JPEG
        img_resized.save(output_path, 'JPEG', quality=85)
        print(f"  ✓ Saved: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading/resizing: {e}")
        return False

def create_placeholder_image(output_path, color_name, size=(256, 256)):
    """Create a placeholder image with text."""
    from PIL import ImageDraw, ImageFont
    
    # Create a simple colored image with text
    img = Image.new('RGB', size, color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Add text
    text = f"{color_name}\n(placeholder)"
    
    # Try to use a font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill='#666666', font=font)
    
    img.save(output_path, 'JPEG', quality=85)
    print(f"  ✓ Created placeholder: {output_path}")

def main():
    # Paths
    base_dir = Path("/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/Colores")
    md_file = base_dir / "Colores.md"
    images_dir = base_dir / "ejemplos"
    
    # Create images directory
    images_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("Color Examples Image Downloader")
    print("=" * 60)
    
    # Extract examples
    print("\n1. Extracting examples from Colores.md...")
    examples = extract_examples_from_markdown(md_file)
    print(f"   Found {len(examples)} color examples")
    
    # Process each example
    print("\n2. Processing images...")
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for i, ex in enumerate(examples, 1):
        color_name = ex['color_name']
        search_term = ex['search_term']
        
        # Create safe filename
        safe_name = re.sub(r'[^\w\s-]', '', color_name.lower())
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        output_file = images_dir / f"{safe_name}.jpg"
        
        print(f"\n[{i}/{len(examples)}] {color_name}")
        
        # Skip if already exists
        if output_file.exists():
            print(f"  ⊙ Already exists: {output_file.name}")
            skip_count += 1
            ex['image_file'] = f"ejemplos/{output_file.name}"
            continue
        
        # Search for images
        image_urls = search_duckduckgo_images(search_term, max_results=3)
        
        # Try to download images
        downloaded = False
        if image_urls:
            for idx, url in enumerate(image_urls):
                print(f"  Trying image {idx + 1}/{len(image_urls)}...")
                if download_and_resize_image(url, output_file):
                    downloaded = True
                    success_count += 1
                    break
        
        # If download failed, create placeholder
        if not downloaded:
            print(f"  Creating placeholder instead...")
            create_placeholder_image(output_file, color_name)
            fail_count += 1
        
        # Store the image filename in the example dict
        ex['image_file'] = f"ejemplos/{output_file.name}"
    
    print("\n" + "=" * 60)
    print("✓ Image processing complete!")
    print(f"  Images saved to: {images_dir}")
    print(f"\nStatistics:")
    print(f"  ✓ Downloaded: {success_count}")
    print(f"  ⊙ Skipped (already exist): {skip_count}")
    print(f"  ✗ Failed (placeholders): {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
