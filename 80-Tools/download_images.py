#!/usr/bin/env python3
"""
Herramienta para descargar imágenes de vocabulario usando LoremFlickr.
Uso: python3 download_images.py --output "ruta/destino"
"""

import os
import argparse
import requests
from PIL import Image
import io
import time
import re

WORD_MAPPING = {
    "afueras": "the outskirts of the city",
    "alrededores": "surroundings",
    "bragas": "woman panties",
    "calzoncillos": "boxers underwear",
    "calzones": "breeches",
    "cosquillas": "tickle",
    "fauces": "wolf jaws",
    "finanzas": "coins calculator",
    "gafas_de_bucear": "scuba mask",
    "ganas": "desire",
    "matematicas": "blackboard math",
    "pantalones": "trousers",
    "pinzas": "tweezers",
    "tenazas": "pincers tool",
    "vacaciones": "vacation luggage",
    "vaqueros": "jeans",
    "vituallas": "the provisions",
}

SPECIFIC_PAGES = {
    "gafas": "https://commons.wikimedia.org/wiki/File:Reading_glasses.jpg",
    "tijeras": "https://commons.wikimedia.org/wiki/File:Standard_scissors.jpg",
    "zapatos": "https://commons.wikimedia.org/wiki/File:A_pair_of_white_shoes.jpg",
    "medias": "https://commons.wikimedia.org/wiki/File:Stockings.jpg",
    "gafas_de_sol": "https://commons.wikimedia.org/wiki/File:Sunglasses-1.jpg",
    "esposas": "https://commons.wikimedia.org/wiki/File:Handcuffs_1.jpg",
    "enseres": "https://commons.wikimedia.org/wiki/File:Kitchen_utensils.jpg",
    "municiones": "https://commons.wikimedia.org/wiki/File:Various_Ammunition.jpg"
}

def get_wikimedia_url(page_url):
    """Scrapes the original file URL from a Wikimedia Commons file page."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Simple extraction: look for the "Original file" link or the main image
        # The main image usually has class="internal" or we check for upload.wikimedia.org links
        # A robust way is finding the link text "Original file" which links to the full res
        
        content = response.text
        # Look for href="...upload.wikimedia.org..." text="Original file"
        # Or simply find the first upload.wikimedia.org link that is NOT a thumb
        
        import re
        # This regex finds links to upload.wikimedia.org that don't assume thumb structure
        # Matches: href="(https://upload.wikimedia.org/wikipedia/commons/[^"]+)"
        # We want to exclude /thumb/ directory if we want original, OR if original is huge we might prefer a large preview?
        # User asked for "512x512 original", so we likely want a reasonable size. 
        # But 'original' on wiki can be 4000px.
        # Let's try to find the "Original file" URL, download it, and resize it.
        
        matches = re.findall(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)"', content)
        
        # Filter out thumbs
        originals = [m for m in matches if "/thumb/" not in m]
        
        if originals:
            return originals[0]
            
        return None
    except Exception as e:
        print(f"  ✗ Error scraping Wikimedia: {e}")
        return None

def download_and_resize(source, output_path, max_size=(512, 512), is_keyword=True):
    """Downloads image from Source (Keyword or URL) and resize it."""
    
    if is_keyword:
        url = f"https://loremflickr.com/512/512/{source.replace(' ', ',')}"
        print(f"Downloading keyword '{source}'...")
    else:
        url = source
        print(f"Downloading from URL...")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  ✓ Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Descargar imágenes para vocabulario.")
    parser.add_argument("--output", required=True, help="Carpeta de destino")
    
    parser.add_argument("--md", help="Archivo markdown para detectar imágenes")
    
    args = parser.parse_args()
    
    output_dir = args.output
    if not os.path.exists(output_dir):
        print(f"Creando directorio: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    total = 0
    
    items_to_process = {} # Dict: filename_stem -> search_query
    
    # Logic:
    # 1. If --md is provided, parse it.
    #    We check for table rows: | **search_query** | ... | ![[.../filename.jpg...]] |
    #    If found, items_to_process[filename] = search_query
    #    If link found but no table match, items_to_process[filename] = filename (fallback)
    
    if args.md:
        print(f"Detecting images from {args.md}...")
        try:
            with open(args.md, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines()
            found_count = 0
            
            # 1. Try to find table rows first
            # Regex: | **(QUERY)** ... ![[.../(FILENAME).jpg...]]
            for line in lines:
                if '![[' in line and '|' in line:
                    # It looks like a table row
                    # Extract bold text between pipes?
                    # Minimal regex for the "Palabra" column
                    # Assumes format: | **word** | ...
                    bold_match = re.search(r'\|\s*\*\*(.*?)\*\*', line)
                    # We expect: | **Word** | Description | ...
                    # Let's parse strictly by splitting pipes
                    parts = [p.strip() for p in line.split('|')]
                    # parts[0] is empty (before first pipe), parts[1] is word, parts[2] is desc
                    
                    if len(parts) >= 4:
                        # Extract Word
                        word_match = re.search(r'\*\*(.*?)\*\*', parts[1])
                        if word_match:
                             word_raw = word_match.group(1).strip()
                        else:
                             word_raw = parts[1] # fallback
                        
                        # Extract Description
                        description = parts[2]
                        
                        # Check for link in any column (usually last?)
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
                                
                                # Combine with Description?
                                # User request: "add also description into search"
                                # We'll start with a simple concat. 
                                # "calzones Ropa interior antigua..."
                                # To avoid too long queries, maybe limit desc chars?
                                # Wikimedia search handles it reasonably. 
                                
                                final_query = f"{query_base} {description}"
                                items_to_process[stem] = final_query
                                found_count += 1
                                continue # Successfully handled this line

            # Simple scan for any missed links (if not in table)
            all_links = re.findall(r'!\[\[(.*?)\]\]', content)
            for raw_link in all_links:
                clean_link = raw_link.split('|')[0]
                filename = os.path.basename(clean_link)
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    stem = os.path.splitext(filename)[0]
                    if stem not in items_to_process:
                         items_to_process[stem] = stem.replace('_', ' ')
                         found_count += 1

            print(f"Found {found_count} images in markdown.")
            
        except Exception as e:
            print(f"Error reading markdown file: {e}")
            return

    else:
        # Legacy mode
        for k in SPECIFIC_PAGES.keys():
            items_to_process[k] = k.replace('_', ' ') # Fallback query
        for k, v in WORD_MAPPING.items():
             if k not in items_to_process:
                items_to_process[k] = v # Use mapped english keyword? Or k?
                # User wants spanish now, but legacy mode implies we use what we have.
                # Let's keep mapped keyword for legacy fallback safety if user doesn't use --md

    # Download Loop
    for word, search_query in items_to_process.items():
        total += 1
        filename = f"{word}.jpg"
        path = os.path.join(output_dir, filename)
        
        if os.path.exists(path):
            print(f"  ✓ {filename} already exists. Skipping.")
            success_count += 1
            continue

        # 1. Search Wikimedia Commons (Deterministic)
        print(f"Searching Wikimedia Commons for '{search_query}'...")
        image_url = search_wikimedia_image(search_query)
        
        if image_url:
             if download_image_from_url(image_url, path):
                success_count += 1
        else:
            # Fallback 1: English Mapping if exists and query was just the spanish word?
            # If query came from Markdown columns ("las gafas"), it's specific.
            # If we fail, maybe we should try without article? Or mapped?
            print(f"  ✗ Failed to find image for '{search_query}'")
            
            # Simple fallback check: if we have a mapping for the 'word' key
            keyword = WORD_MAPPING.get(word)
            if keyword and keyword != search_query:
                 print(f"    Trying english keyword '{keyword}'...")
                 image_url = search_wikimedia_image(keyword)
                 if image_url and download_image_from_url(image_url, path):
                     success_count += 1

        
        # Be nice to the server
        time.sleep(0.5) 

    print(f"\n✓ Completado: {success_count}/{total} imágenes procesadas.")

def search_wikimedia_image(query, limit=5):
    """Searches Wikimedia Commons and returns the FIRST valid URL (Deterministic)."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6", # File namespace
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    headers = {
        "User-Agent": "VocabTools/1.0 (Contact: user@example.com)" 
    }
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        # We need to sort or find the 'first' result.
        # The API "generator=search" returns pages dict keyed by ID.
        # The order in the dict isn't guaranteed to be relevance order in Python < 3.7 (though likely is in modern).
        # But 'index' property is usually available if we use 'list=search' instead?
        # generator=search might not preserve order in the dictionary keys easily if we just iterate items().
        
        # However, typically 'gsroffset' etc apply.
        # Let's verify if 'index' is returned.
        # Actually generator results are a bit tricky for order.
        
        # BETTER APPROACH for deterministic relevance:
        # Use action=query&list=search getting title, then query imageinfo for title.
        # A simpler way with generator: The 'index' field usually exists in the result? 
        # API documentation says generator results are "unordered" in the map but usually we want the top one.
        
        # If we just want "a result" and "do not randomize", picking the first from list(pages.values()) is deterministic per execution but maybe not highly relevant?
        # Actually, let's switch to list=search for order safety?
        # Or just assume pages list is okay if we sort by 'index' if present.
        
        # Let's iterate and pick the first valid JPG/PNG.
        
        sorted_pages = sorted(pages.values(), key=lambda x: x.get('index', 0))
        
        for page_data in sorted_pages:
            imageinfo = page_data.get("imageinfo", [])
            if imageinfo:
                u = imageinfo[0]["url"]
                if u.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"  Selected: {u}")
                    return u
        
        print("  ⚠ No valid images found in search results.")
        return None

    except Exception as e:
        print(f"  ✗ Error searching Wikimedia: {e}")
        return None

def download_image_from_url(url, output_path, max_size=(512, 512)):
    """Downloads image from a specific URL and resizes it."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Timeout 10s for download
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  ✓ Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading/saving: {e}")
        return False

if __name__ == "__main__":
    main()
