import os
import re

def fix_ciudad():
    path = "30-Vocabulario/Temas/La Ciudad y el Barrio.md"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace attachments path
    content = content.replace("../attachments/la_ciudad_y_el_barrio/", "La Ciudad y el Barrio/")
    # Remove |100 sizing (user might prefer the default 512x512)
    content = content.replace("\\|100", "")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed La Ciudad y el Barrio.md")

def fix_profesiones():
    path = "30-Vocabulario/Temas/Profesiones.md"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix mecanico.jpg
    content = content.replace("![[mecanico.jpg]]", "![[Profesiones/mecanico.jpg]]")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed Profesiones.md")

if __name__ == "__main__":
    fix_ciudad()
    fix_profesiones()
