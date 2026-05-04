import os
import re

def parse_and_add(filepath, new_rows_dict, target_section_header=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    out_lines = []
    in_table = False
    table_lines = []
    current_section = None
    
    # Pre-collect existing words across the whole file to avoid adding if they exist anywhere
    all_existing_esp = set()
    for line in lines:
        if line.strip().startswith('|') and '|' in line[1:]:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 2 and 'Término' not in cols[1]:
                esp_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', cols[1]).strip()
                all_existing_esp.add(esp_clean.lower())

    # Keep track of words we have successfully added so we don't add them to multiple tables
    added_words = set()

    for line in lines:
        if line.startswith('## '):
            current_section = line.strip()
            
        if line.strip().startswith('|') and '|' in line[1:]:
            in_table = True
            table_lines.append(line)
        else:
            if in_table:
                header = table_lines[0]
                separator = table_lines[1]
                rows = table_lines[2:]
                
                if 'Término' in header and (target_section_header is None or current_section == target_section_header):
                    parsed_rows = []
                    for r in rows:
                        cols = [c.strip() for c in r.split('|')[1:-1]]
                        if len(cols) >= 2:
                            esp_raw = cols[1]
                            esp_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', esp_raw).strip()
                            parsed_rows.append((esp_clean, r))
                    
                    folder = os.path.basename(filepath).replace('.md', '')
                    for esp, data in new_rows_dict.items():
                        if esp in added_words:
                            continue
                        main_word = esp.split('/')[0].strip().lower()
                        if not any(main_word in e for e in all_existing_esp):
                            img_name = data.get('img', '')
                            img_col = f"![[{folder}/{img_name}]]" if img_name else ""
                            headers = [h.strip() for h in header.split('|')[1:-1]]
                            new_cols = []
                            for h in headers:
                                if h == 'Imagen': new_cols.append(img_col)
                                elif h == 'Término': new_cols.append(f"**{esp}**")
                                elif h == 'Traducción': new_cols.append(data.get('trad', ''))
                                elif h == 'Descripción en español': new_cols.append(data.get('desc', ''))
                                elif h == 'Ingredientes': new_cols.append(data.get('ingr', ''))
                                else: new_cols.append("")
                            new_row = "| " + " | ".join(new_cols) + " |"
                            parsed_rows.append((esp, new_row))
                            all_existing_esp.add(esp.lower())
                            added_words.add(esp)
                    
                    parsed_rows.sort(key=lambda x: x[0].lower().replace('el ', '').replace('la ', '').replace('los ', '').replace('las ', ''))
                    
                    out_lines.append(header)
                    out_lines.append(separator)
                    for _, r in parsed_rows:
                        out_lines.append(r)
                else:
                    out_lines.extend(table_lines)
                
                table_lines = []
                in_table = False
            out_lines.append(line)
            
    if in_table:
        out_lines.extend(table_lines)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))


# 1. Frutas y Verduras
frutas = {
    'el tomate': {'img': 'tomate.jpg', 'trad': 'tomato / помидор', 'desc': 'Fruta roja; se usa como verdura en el gazpacho.'},
    'la fresa': {'img': 'fresa.jpg', 'trad': 'strawberry / клубника', 'desc': 'Fruta roja pequeña; típica en primavera.'},
    'la manzana': {'img': 'manzana.jpg', 'trad': 'apple / яблоко', 'desc': 'Fruta muy común; puede ser roja o verde.'},
    'el níspero': {'img': 'nispero.jpg', 'trad': 'loquat / мушмула', 'desc': 'Fruta de primavera; color naranja y dulce.'},
    'la naranja': {'img': 'naranja.jpg', 'trad': 'orange / апельсин', 'desc': 'Cítrico dulce; famoso el zumo de naranja de Valencia.'},
    'la ciruela': {'img': 'ciruela.jpg', 'trad': 'plum / слива', 'desc': 'Fruta redonda; muy buena para la digestión.'}
}
parse_and_add('30-Vocabulario/Temas/Comida - Frutas y Verduras.md', frutas, target_section_header='## Frutas')

# 2. Platos y Tapas
platos = {
    'el bacalao encebollado': {'img': 'bacalao_encebollado.jpg', 'trad': 'cod with onions / треска с луком', 'desc': 'Plato tradicional; el bacalao se cocina con mucha cebolla.', 'ingr': 'Bacalao, cebolla, aceite, sal.'},
    'la empanada gallega': {'img': 'empanada_gallega.jpg', 'trad': 'Galician pie / галисийский пирог', 'desc': 'Pastel salado; típico de Galicia.', 'ingr': 'Masa, atún, tomate, cebolla, pimiento.'},
    'la tortilla de berenjena': {'img': 'tortilla_berenjena.jpg', 'trad': 'eggplant omelette / омлет с баклажанами', 'desc': 'Variante de la tortilla; más ligera que la de patata.', 'ingr': 'Huevos, berenjena, aceite, sal.'},
    'la crema de calabaza': {'img': 'crema_calabaza.jpg', 'trad': 'pumpkin cream / тыквенный крем-суп', 'desc': 'Sopa caliente; muy típica en otoño.', 'ingr': 'Calabaza, patata, cebolla, aceite, sal.'},
    'la ensalada murciana': {'img': 'ensalada_murciana.jpg', 'trad': 'Murcian salad / мурсийский салат', 'desc': 'Ensalada tradicional; plato típico de Murcia.', 'ingr': 'Tomate, atún, huevo, cebolla, aceitunas.'},
    'la magra con tomate': {'img': 'magra_tomate.jpg', 'trad': 'lean pork with tomato / нежирная свинина с томатами', 'desc': 'Tapa caliente; carne de cerdo guisada en salsa de tomate.', 'ingr': 'Cerdo, tomate frito, aceite, sal.'},
    'el consomé con pelotas': {'img': 'consome_pelotas.jpg', 'trad': 'consommé with meatballs / бульон с фрикадельками', 'desc': 'Sopa caliente; se come mucho en Navidad en el este de España.', 'ingr': 'Caldo de carne, carne picada, pan, huevo.'},
    'el arroz con costra': {'img': 'arroz_costra.jpg', 'trad': 'rice with crust / рис с корочкой', 'desc': 'Plato de arroz; cubierto con huevo batido al horno, típico de Alicante.', 'ingr': 'Arroz, carne, embutido, huevos.'},
    'el arroz con conejo': {'img': 'arroz_conejo.jpg', 'trad': 'rice with rabbit / рис с кроликом', 'desc': 'Arroz tradicional; muy común en la montaña.', 'ingr': 'Arroz, conejo, caracoles, verduras.'},
    'el estofado de ternera': {'img': 'estofado_ternera.jpg', 'trad': 'beef stew / тушеная говядина', 'desc': 'Guiso caliente; comida casera tradicional.', 'ingr': 'Ternera, patata, zanahoria, cebolla.'},
    'las natillas': {'img': 'natillas.jpg', 'trad': 'custard / заварной крем', 'desc': 'Postre cremoso; suele llevar canela por encima.', 'ingr': 'Leche, yemas de huevo, azúcar, vainilla.'},
    'el tiramisú': {'img': 'tiramisu.jpg', 'trad': 'tiramisu / тирамису', 'desc': 'Postre italiano; muy popular en España.', 'ingr': 'Queso mascarpone, café, cacao, bizcochos.'},
    'la macedonia': {'img': 'macedonia.jpg', 'trad': 'fruit salad / фруктовый салат', 'desc': 'Postre fresco; ensalada de frutas de temporada.', 'ingr': 'Variedad de frutas troceadas.'},
    'los chopitos': {'img': 'chopitos.jpg', 'trad': 'fried baby squid / жареные маленькие кальмары', 'desc': 'Tapa de marisco frito; muy típica en bares.', 'ingr': 'Calamaritos, harina, aceite.'},
    'el pepito de ternera': {'img': 'pepito_ternera.jpg', 'trad': 'beef sandwich / сэндвич с говядиной', 'desc': 'Bocadillo caliente; muy popular para cenar.', 'ingr': 'Pan, filete de ternera, aceite.'}
}
parse_and_add('30-Vocabulario/Temas/Comida - Platos y Tapas.md', platos)

print("Food updates completed successfully.")
