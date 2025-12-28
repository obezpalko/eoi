#!/usr/bin/env python3
"""
Herramienta para descargar imágenes de vocabulario usando DuckDuckGo.
Uso: python3 download_images.py --output "ruta/destino" --md "archivo.md"
"""

import os
import argparse
import requests
from PIL import Image
import io
import time
import re
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

def search_ddg_image(query, max_results=5):
    """Searches DuckDuckGo for images and returns the first valid URL."""
    try:
        print(f"  Searching DuckDuckGo for '{query}'...")
        ddgs = DDGS()
        results = ddgs.images(
            keywords=query,
            max_results=max_results,
            safesearch='moderate',
            size='Medium',  # Medium size images
            type_image=None
        )
        
        for result in results:
            url = result.get('image')
            if url and any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                print(f"    Found: {url[:80]}...")
                return url
        
        print(f"  ⚠ No valid images found for '{query}'")
        return None
        
    except Exception as e:
        print(f"  ✗ Error searching DuckDuckGo: {e}")
        return None

def download_image_from_url(url, output_path, max_size=(512, 512)):
    """Downloads image from a specific URL and resizes it."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  ✓ Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading/saving: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Descargar imágenes para vocabulario usando DuckDuckGo.")
    parser.add_argument("--output", required=True, help="Carpeta de destino")
    parser.add_argument("--md", required=True, help="Archivo markdown para detectar imágenes")
    
    args = parser.parse_args()
    
    output_dir = args.output
    if not os.path.exists(output_dir):
        print(f"Creando directorio: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    total = 0
    
    items_to_process = {}  # Dict: filename_stem -> search_query
    
    print(f"Detecting images from {args.md}...")
    try:
        with open(args.md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        found_count = 0
        
        # Parse table rows to extract profession name and description
        for line in lines:
            if '![[' in line and '|' in line:
                # It looks like a table row
                parts = [p.strip() for p in line.split('|')]
                
                if len(parts) >= 5:  # Expected format: | **word** | masc | fem | description | image |
                    # Extract profession name (column 1)
                    word_match = re.search(r'\*\*(.*?)\*\*', parts[1])
                    if word_match:
                        word_raw = word_match.group(1).strip()
                    else:
                        word_raw = parts[1].strip()
                    
                    # Extract Description (column 4)
                    description = parts[4].strip()
                    
                    # Extract image link
                    link_match = re.search(r'!\[\[(.*?)\]\]', line)
                    
                    if link_match:
                        raw_link = link_match.group(1)
                        clean_link = raw_link.split('|')[0]
                        filename = os.path.basename(clean_link)
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                            stem = os.path.splitext(filename)[0]
                            
                            # Clean Query (Strip articles)
                            query_base = word_raw
                            for art in ["el ", "la ", "los ", "las "]:
                                if query_base.lower().startswith(art):
                                    query_base = query_base[len(art):]
                                    break
                            
                            # Create search query: profession name + description for better results
                            # For professions, add "profesión" to get better images
                            final_query = f"{query_base} profesión {description}"
                            items_to_process[stem] = final_query
                            found_count += 1

        print(f"Found {found_count} images in markdown.\n")
        
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return

    # Download Loop
    for word, search_query in items_to_process.items():
        total += 1
        filename = f"{word}.jpg"
        path = os.path.join(output_dir, filename)
        
        if os.path.exists(path):
            print(f"✓ {filename} already exists. Skipping.")
            success_count += 1
            continue

        print(f"\n[{total}/{len(items_to_process)}] Processing: {word}")
        
        # Search DuckDuckGo
        image_url = search_ddg_image(search_query)
        
        if image_url:
            if download_image_from_url(image_url, path):
                success_count += 1
            else:
                # Try simpler query without description
                print(f"  Retrying with simpler query...")
                simple_query = word.replace('_', ' ') + " profession"
                image_url = search_ddg_image(simple_query)
                if image_url and download_image_from_url(image_url, path):
                    success_count += 1
        else:
            print(f"  ✗ Failed to find image for '{search_query}'")
        
        # Be nice to the server
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"✓ Completado: {success_count}/{total} imágenes procesadas.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

