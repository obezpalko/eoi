import sys
import os
from PIL import Image

# Add 80-Tools to path
sys.path.append(os.path.abspath("80-Tools"))
from download_images_universal import search_ddg_images, download_and_resize_image

def redownload():
    output_dir = "30-Vocabulario/Temas/La Ciudad y el Barrio"
    items = [
        ("la_cafeteria", "cafetería building facade coffee shop exterior"),
        ("el_colegio", "colegio building facade school exterior"),
        ("la_drogueria", "droguería shop front cleaning supplies store"),
        ("correos", "oficina de correos building facade post office spain"),
        ("la_farmacia", "farmacia building facade pharmacy spain"),
        ("la_floristeria", "floristería shop front flower shop exterior"),
        ("el_instituto", "instituto building facade high school exterior"),
        ("la_panaderia", "panadería building facade bakery storefront"),
        ("la_peluqueria", "peluquería shop front hair salon exterior"),
        ("la_fuente", "fuente ciudad city fountain monument"),
        ("urgencias", "entrada urgencias hospital emergency room entrance")
    ]
    
    for filename, query in items:
        print(f"Redownloading {filename} with query: {query}")
        target_path = os.path.join(output_dir, f"{filename}.jpg")
        # Remove old one if exists
        if os.path.exists(target_path):
            os.remove(target_path)
            
        urls = search_ddg_images(query, max_results=5)
        success = False
        for url in urls:
            if download_and_resize_image(url, target_path, max_size=(512, 512)):
                success = True
                break
        
        if success:
            print(f"  ✓ Updated {filename}")
        else:
            print(f"  ✗ Failed {filename}")

if __name__ == "__main__":
    redownload()
