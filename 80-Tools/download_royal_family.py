#!/usr/bin/env python3
"""
Descarga imágenes de la Familia Real Española usando la API de Wikipedia.
Redimensiona automáticamente a 144px (thumbnail).
"""

import os
import requests
import time

# Mapa de Nombre en Archivo -> Título de Wikipedia (EN o ES según disponibilidad, EN suele tener mejores infobox images standard)
# Usaremos la API en inglés en general.
PEOPLE = {
    "JC": "Juan Carlos I of Spain",
    "Sofia": "Queen Sofía of Spain",
    "Felipe": "Felipe VI of Spain",
    "Letizia": "Queen Letizia of Spain",
    "Leonor": "Leonor, Princess of Asturias",
    "SofiaHija": "Infanta Sofía of Spain",
    "Elena": "Infanta Elena, Duchess of Lugo",
    "Cristina": "Infanta Cristina of Spain",
    "Jaime": "Jaime de Marichalar",
    "Inaki": "Iñaki Urdangarin",
    "Froilan": "Felipe de Marichalar y Borbón",
}

# Archivos específicos de Wikimedia Commons cuando la búsqueda simple falla o no hay foto personal
# (Para los hijos Urdangarin usamos sus escudos/coats of arms si no hay foto)
MANUAL_FILES = {
    "Victoria": "File:Victoria_Federica_de_Marichalar_y_de_Borbón_(cropped).png",
    "JuanU": "File:Coat_of_Arms_of_Juan_Valentín_Urdangarin,_Grandee_of_Spain.svg",
    "Pablo": "File:Coat_of_Arms_of_Pablo_Nicolás_Urdangarín,_Grandee_of_Spain.svg",
    "Miguel": "File:Coat_of_Arms_of_Miguel_Urdangarín,_Grandee_of_Spain.svg",
    "Irene": "File:Coat_of_Arms_of_Irene_Urdangarín,_Grandee_of_Spain.svg",
    "JC": "File:Juan_Carlos_I_of_Spain_2007.jpg",
    "Felipe": "File:King_Felipe_VI_of_Spain.jpg"
}

OUTPUT_DIR = "/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/Familia del rey"

def download_file_by_name(name_key, filename_wiki):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": filename_wiki,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 144, # Thumbnail size
        "format": "json"
    }

    try:
        print(f"Descargando archivo manual: {filename_wiki}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "imageinfo" in page_data:
                img_url = page_data["imageinfo"][0]["thumburl"]
                # Si es SVG y pedimos thumb, Wikipedia da PNG. Si no, da el original si es pequeño o el thumb.
                # Para SVGs, thumburl suele ser un PNG rasterizado, lo cual es perfecto para nuestro SVG generator que usa base64 jpg/png.
                
                print(f"  -> URL manual encontrada: {img_url}")
                img_r = requests.get(img_url, headers=headers, timeout=10)
                
                # Determinar extensión (siempre png para thumbs de svg, o jpg)
                ext = img_url.split('.')[-1]
                if len(ext) > 4: ext = "jpg"
                
                filename = f"{name_key}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_r.content)
                print(f"  -> Guardado en {filename}")
                return filename
            else:
                print(f"  -> No se encontró info de imagen para {filename_wiki}")
    except Exception as e:
        print(f"Error procesando manual {filename_wiki}: {e}")


def download_image(name_key, wiki_title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": wiki_title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 144
    }

    try:
        print(f"Buscando: {wiki_title}...")
        # Wikipedia requires a User-Agent with contact info to allow bots.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check for non-JSON response (likely an error page)
        try:
            data = r.json()
        except Exception:
            print(f"  ✗ Error: La respuesta no es JSON valid (Posible bloqueo por User-Agent).")
            print(f"    Contenido: {r.text[:100]}...")
            return None
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "thumbnail" in page_data:
                img_url = page_data["thumbnail"]["source"]
                # Descargar
                print(f"  -> URL encontrada: {img_url}")
                img_r = requests.get(img_url, headers=headers, timeout=10)
                
                ext = img_url.split('.')[-1].split('?')[0] # simple extension guess
                if len(ext) > 4: ext = "jpg" # fallback
                
                filename = f"{name_key}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_r.content)
                print(f"  -> Guardado en {filename}")
                return filename
            else:
                print(f"  -> No se encontró thumbnail para {wiki_title}")
    except Exception as e:
        print(f"Error procesando {wiki_title}: {e}")
    
    return None

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for key, title in PEOPLE.items():
        download_image(key, title)
        time.sleep(0.5) 
        
    print("--- Procesando archivos manuales ---")
    for key, filename in MANUAL_FILES.items():
        download_file_by_name(key, filename)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
