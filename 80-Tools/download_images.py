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

WORD_MAPPING = {
    "gafas": "glasses",
    "tijeras": "scissors",
    "pantalones": "trousers",
    "bragas": "panties",
    "calzoncillos": "boxers underwear",
    "calzones": "bloomers",
    "vaqueros": "jeans",
    "zapatos": "shoes",
    "medias": "stockings",
    "gafas_de_sol": "sunglasses",
    "gafas_de_bucear": "scuba goggles",
    "tenazas": "pincers tool",
    "pinzas": "tweezers",
    "esposas": "handcuffs",
    "vacaciones": "vacation beach",
    "cosquillas": "feather tickle",
    "ganas": "craving food",
    "fauces": "jaws animal",
    "enseres": "household items",
    "vituallas": "food provisions",
    "finanzas": "finance money",
    "matematicas": "mathematics",
    "alrededores": "landscape surroundings",
    "afueras": "suburbs",
    "municiones": "ammunition"
}

def download_and_resize(keyword, output_path, max_size=(144, 144)):
    """Downloads image from LoremFlickr and resize it."""
    # LoremFlickr allows specifying size in URL: https://loremflickr.com/width/height/keyword
    # We request a slightly larger random image to ensure quality if we need to crop/resize, 
    # but practically requesting 144/144 directly is most efficient if valid.
    # To be safe, let's ask for the exact size.
    # Note: LoremFlickr searches matching the keywords.
    
    url = f"https://loremflickr.com/144/144/{keyword.replace(' ', ',')}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Downloading {keyword} to {output_path}...")
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Ensure it fits max_size (though we requested 144x144, the service might differ slightly or we want to be sure)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        img.save(output_path, "JPEG", quality=85, optimize=True)
        print(f"  ✓ Saved")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Descargar imágenes para vocabulario.")
    parser.add_argument("--output", required=True, help="Carpeta de destino")
    
    args = parser.parse_args()
    
    output_dir = args.output
    if not os.path.exists(output_dir):
        print(f"Creando directorio: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    total = 0
    
    for word, keyword in WORD_MAPPING.items():
        total += 1
        filename = f"{word}.jpg"
        path = os.path.join(output_dir, filename)
        
        # We assume we want to overwrite to update existing ones (or create new ones)
        if download_and_resize(keyword, path):
            success_count += 1
        
        # Be nice to the server
        time.sleep(0.5)

    print(f"\n✓ Completado: {success_count}/{total} imágenes descargadas.")

if __name__ == "__main__":
    main()
