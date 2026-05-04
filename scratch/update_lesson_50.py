import os
import re

# 1. UPDATE LESSON TEXT
lesson_file = '10-Lecciones/20260429 Lección cincuenta.md'
with open(lesson_file, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '# 050: Lección template': '# 050: La Comida y el Imperativo',
    'prescripción': 'preinscripción',
    '- plátano (banana is wrong )': '- plátano (la palabra "banana" no se usa en España)',
    '- Carlota (zanahoria )': '- carlota (zanahoria en la Comunidad Valenciana)',
    'la manzana está verde/maduro': 'la manzana está verde/madura',
    'estoy moreno.': 'estoy morena.',
    'está pera está': 'esta pera está',
    'patas fritas (patatis)': 'patatas fritas',
    'en un inmobiliario': 'en una inmobiliaria',
    'Plato, ración, tapa (size)': 'Plato, ración, tapa (tamaños)',
    'Crema d calabaza': 'Crema de calabaza',
    'Tarta de abuela ?': 'Tarta de la abuela',
    'Macedonia ?': 'Macedonia (ensalada de frutas)',
    '- galletas con cukies?': '- galletas con pepitas de chocolate (cookies)',
    '- chopitos VS chupito': '- chopitos (calamares pequeños) vs. chupito (vaso pequeño de alcohol)'
}

for old, new in replacements.items():
    text = text.replace(old, new)

with open(lesson_file, 'w', encoding='utf-8') as f:
    f.write(text)

# 2. UPDATE VOCABULARY TABLES
def add_to_table(filepath, new_rows_dict):
    """
    new_rows_dict: { 'Español': ('Inglés', 'Ruso', 'image_filename.jpg') }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We find tables by looking for '| :---'
    # Actually, let's just parse the lines.
    lines = content.split('\n')
    out_lines = []
    in_table = False
    table_lines = []
    
    for line in lines:
        if line.strip().startswith('|') and '|' in line[1:]:
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                # process table
                header = table_lines[0]
                separator = table_lines[1]
                rows = table_lines[2:]
                
                # Check if it's the right table (has Español)
                if 'Español' in header:
                    existing_esp = set()
                    parsed_rows = []
                    for r in rows:
                        cols = [c.strip() for c in r.split('|')[1:-1]]
                        if len(cols) >= 2:
                            # Usually cols[1] is Español (cols[0] is Imagen)
                            # Let's extract the bold text if any
                            esp_raw = cols[1]
                            esp_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', esp_raw).strip()
                            existing_esp.add(esp_clean.lower())
                            parsed_rows.append((esp_clean, r))
                    
                    # Add new rows
                    folder = os.path.basename(filepath).replace('.md', '')
                    for esp, (ing, rus, img_name) in new_rows_dict.items():
                        # We just check the main word to avoid duplicates
                        main_word = esp.split('/')[0].strip().lower()
                        if not any(main_word in e for e in existing_esp):
                            img_col = f"![[{folder}/{img_name}]]" if img_name else ""
                            # Format assuming: Imagen | Español | Inglés | Ruso
                            # We check header columns to be sure
                            headers = [h.strip() for h in header.split('|')[1:-1]]
                            new_cols = []
                            for h in headers:
                                if h == 'Imagen': new_cols.append(img_col)
                                elif h == 'Español': new_cols.append(f"**{esp}**")
                                elif h == 'Inglés': new_cols.append(ing)
                                elif h == 'Ruso': new_cols.append(rus)
                                else: new_cols.append("")
                            new_row = "| " + " | ".join(new_cols) + " |"
                            parsed_rows.append((esp, new_row))
                            existing_esp.add(esp.lower())
                    
                    # Sort alphabetically by Español
                    parsed_rows.sort(key=lambda x: x[0].lower().replace('el ', '').replace('la ', '').replace('los ', '').replace('las ', ''))
                    
                    out_lines.append(header)
                    out_lines.append(separator)
                    for _, r in parsed_rows:
                        out_lines.append(r)
                else:
                    # not a vocab table, just output as is
                    out_lines.extend(table_lines)
                
                table_lines = []
                in_table = False
            out_lines.append(line)
            
    if in_table:
        out_lines.extend(table_lines)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))


# LA CIUDAD Y EL BARRIO
tiendas = {
    'La carnicería': ('Butcher shop', 'Мясной магазин', 'la_carniceria.jpg'),
    'La charcutería': ('Delicatessen', 'Магазин колбас и сыров', 'la_charcuteria.jpg'),
    'La frutería': ('Greengrocer', 'Овощной магазин', 'la_fruteria.jpg'),
    'La inmobiliaria': ('Real estate agency', 'Агентство недвижимости', 'la_inmobiliaria.jpg'),
    'La juguetería': ('Toy store', 'Магазин игрушек', 'la_jugueteria.jpg'),
    'La parafarmacia': ('Parapharmacy', 'Парафармация', 'la_parafarmacia.jpg'),
    'La perfumería': ('Perfume shop', 'Парфюмерный магазин', 'la_perfumeria.jpg'),
    'La pescadería': ('Fishmonger', 'Рыбный магазин', 'la_pescaderia.jpg'),
    'La pollería': ('Poultry shop', 'Магазин птицы', 'la_polleria.jpg'),
    'El quiosco': ('Kiosk', 'Киоск', 'el_quiosco.jpg'),
    'La tienda de comestibles': ('Grocery store', 'Продуктовый магазин', 'la_tienda_de_comestibles.jpg')
}
add_to_table('30-Vocabulario/Temas/La Ciudad y el Barrio.md', tiendas)

print("Updates completed successfully.")
