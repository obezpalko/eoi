#!/usr/bin/env python3
"""Download Christmas in Spain images using DuckDuckGo image search."""

import os
import requests
from PIL import Image
import io
import time
import re

OUTPUT_DIR = "/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/Navidad en España"

IMAGES = {
    "reyes_magos.jpg": "Reyes Magos Melchor Gaspar Baltasar",
    "cabalgata.jpg": "cabalgata reyes magos parade spain",
    "roscon_de_reyes.jpg": "roscon de reyes cake spain",
    "carta_reyes.jpg": "carta reyes magos letter christmas",
    "belen.jpg": "nativity scene christmas belen",
}

def search_ddg_image(query, max_results=5):
    """Search DuckDuckGo for images using ddgs library."""
    try:
        from ddgs import DDGS
        
        ddgs = DDGS()
        results = list(ddgs.images(query, max_results=max_results))
        
        for r in results:
            img_url = r.get('image')
            if img_url:
                return img_url
        
        return None
        
    except ImportError:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.images(query, max_results=max_results))
                for r in results:
                    img_url = r.get('image')
                    if img_url:
                        return img_url
            return None
        except Exception as e:
            print(f"  DDG import error: {e}")
            return None
    except Exception as e:
        print(f"  DDG search error: {e}")
        return None

def search_wikimedia_image(query, limit=5):
    """Search Wikimedia Commons for images."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    headers = {"User-Agent": "NavidadTools/1.0"}
    
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        pages = data.get("query", {}).get("pages", {})
        sorted_pages = sorted(pages.values(), key=lambda x: x.get('index', 0))
        
        for page_data in sorted_pages:
            imageinfo = page_data.get("imageinfo", [])
            if imageinfo:
                u = imageinfo[0]["url"]
                if u.lower().endswith(('.jpg', '.jpeg', '.png')):
                    return u
        return None
    except Exception as e:
        print(f"  Wikimedia search error: {e}")
        return None

def download_and_resize(url, output_path, max_size=(500, 400)):
    """Download image and resize."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=85)
        print(f"  ✓ Saved: {os.path.basename(output_path)} ({img.size[0]}x{img.size[1]})")
        return True
    except Exception as e:
        print(f"  ✗ Download error: {e}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Downloading Christmas in Spain images...\n")
    
    for filename, query in IMAGES.items():
        path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(path):
            print(f"✓ {filename} already exists")
            continue
        
        print(f"Searching for '{query}'...")
        
        # Use DDG as primary source
        url = search_ddg_image(query)
        
        if not url:
            # Fallback to Wikimedia
            print("  Trying Wikimedia...")
            url = search_wikimedia_image(query)
        
        if url:
            print(f"  Found: {url[:80]}...")
            download_and_resize(url, path)
        else:
            print(f"  ✗ No image found for {filename}")
        
        time.sleep(1)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
