#!/usr/bin/env python3
"""Download missing profession images with longer delays."""

import os
import time
import requests
from PIL import Image
import io

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

MISSING_IMAGES = {
    'dependiente': 'dependiente tienda vendedor trabajando',
    'empresario': 'empresario hombre negocios traje',
    'fotografo': 'fotógrafo cámara profesional',
    'funcionario': 'funcionario oficina trabajador público',
    'guia_turistico': 'guía turístico grupo turistas',
    'maestro': 'maestro profesor niños escuela primaria',
    'modelo': 'modelo pasarela moda',
    'psicologo': 'psicólogo terapeuta sesión',
    'taxista': 'taxista conductor taxi',
    'veterinario': 'veterinario doctor animal perro gato'
}

def search_ddg_image(query):
    """Search DuckDuckGo for images."""
    try:
        print(f"  Searching for '{query}'...")
        ddgs = DDGS()
        results = ddgs.images(
            query,  # First positional argument
            max_results=5,
            safesearch='moderate',
            size='Medium'
        )
        
        for result in results:
            url = result.get('image')
            if url and any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                print(f"    Found: {url[:60]}...")
                return url
        
        return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def download_image(url, output_path):
    """Download and resize image."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  ✓ Saved!")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading: {e}")
        return None

def main():
    output_dir = "30-Vocabulario/Temas/Profesiones"
    success = 0
    
    print(f"Downloading {len(MISSING_IMAGES)} missing profession images...\n")
    
    for i, (filename, query) in enumerate(MISSING_IMAGES.items(), 1):
        print(f"[{i}/{len(MISSING_IMAGES)}] {filename}")
        
        path = os.path.join(output_dir, f"{filename}.jpg")
        if os.path.exists(path):
            print(f"  ✓ Already exists. Skipping.")
            success += 1
            continue
        
        url = search_ddg_image(query)
        if url and download_image(url, path):
            success += 1
        
        # Longer delay to avoid rate limiting
        if i < len(MISSING_IMAGES):
            print(f"  Waiting 3 seconds...")
            time.sleep(3)
        print()
    
    print(f"{'='*60}")
    print(f"✓ Downloaded: {success}/{len(MISSING_IMAGES)} images")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

