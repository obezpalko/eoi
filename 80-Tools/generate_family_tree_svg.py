#!/usr/bin/env python3
"""
Genera un arbol genealógico en SVG incrustando las imágenes presentes en el directorio.
"""
import os
import base64

TARGET_DIR = "/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/Familia del rey"
OUTPUT_FILE = os.path.join(TARGET_DIR, "arbol_genealogico.svg")

# Conf
NODE_WIDTH = 100
NODE_HEIGHT = 130
IMG_SIZE = 80
X_GAP = 20
Y_GAP = 100

def get_base64_image(filename):
    path = os.path.join(TARGET_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')

def node_xml(x, y, label, img_filename=None, sublabel=""):
    img_b64 = get_base64_image(img_filename) if img_filename else None
    
    xml = f'<g transform="translate({x},{y})">'
    
    # Background box
    xml += f'<rect x="0" y="0" width="{NODE_WIDTH}" height="{NODE_HEIGHT}" rx="10" fill="#f0f0f0" stroke="#ccc" />'
    
    # Image
    if img_b64:
        xml += f'<image x="{(NODE_WIDTH-IMG_SIZE)/2}" y="10" width="{IMG_SIZE}" height="{IMG_SIZE}" href="{img_b64}" clip-path="inset(0% round 50%)" />'
    else:
        # Placeholder circle
        xml += f'<circle cx="{NODE_WIDTH/2}" cy="{10+IMG_SIZE/2}" r="{IMG_SIZE/2}" fill="#ddd" />'
        
    # Text
    xml += f'<text x="{NODE_WIDTH/2}" y="{IMG_SIZE+25}" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">{label}</text>'
    if sublabel:
        xml += f'<text x="{NODE_WIDTH/2}" y="{IMG_SIZE+40}" font-family="Arial" font-size="10" text-anchor="middle" fill="#666">{sublabel}</text>'
        
    xml += '</g>'
    return xml, (x + NODE_WIDTH/2, y) # Return top-center (actually usually we want bottom center for parenting, let's just use known coords)

def line_xml(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#666" stroke-width="2" />'

def main():
    svg_content = ""
    
    # --- Layout Setup ---
    # Width calc: 3 main branches. 
    # Left (Elena): 2 children -> need space for ~2 nodes width
    # Center (Cristina): 4 children -> need space for ~4 nodes width
    # Right (Felipe): 2 children -> need space for ~2 nodes width
    
    # Coordinates (rough grid)
    # Row 1: Grandparents (Center)
    ROW1_Y = 50
    # Row 2: Parents
    ROW2_Y = 250
    # Row 3: Children
    ROW3_Y = 450
    
    # Horizontal spacing units
    U = NODE_WIDTH + X_GAP # Unit width
    
    # Center point
    CX = 6 * U 
    
    # --- Nodes ---
    nodes = [] # list of strings
    lines = [] # list of strings

    # Row 1: JC & Sofia
    # Place them centered
    lines.append(line_xml(CX-U/2 + NODE_WIDTH/2, ROW1_Y + NODE_HEIGHT/2, CX+U/2 + NODE_WIDTH/2, ROW1_Y + NODE_HEIGHT/2)) # Marriage line
    
    n_jc = node_xml(CX - U/2, ROW1_Y, "Juan Carlos I", "JC.jpg", "Rey Emérito")
    n_so = node_xml(CX + 0.6*U, ROW1_Y, "Sofía", "Sofia.jpg", "Reina Emérita")
    
    nodes.append(n_jc[0])
    nodes.append(n_so[0])
    
    # Origin point for children lines (center of marriage line)
    ORIGIN_X = CX + NODE_WIDTH/2
    ORIGIN_Y = ROW1_Y + NODE_HEIGHT
    
    # --- Families ---
    
    # Branch 1: Elena (Left)
    # Pos: Left side
    BX1 = 2 * U
    
    lines.append(line_xml(ORIGIN_X, ORIGIN_Y, BX1 + NODE_WIDTH/2, ROW2_Y)) # Line from grandparents
    
    n_elen = node_xml(BX1, ROW2_Y, "Elena", "Elena.jpg", "Infanta")
    n_jaim = node_xml(BX1 + 1.2*U, ROW2_Y, "Jaime", "Jaime.jpg", "Ex-esposo")
    lines.append(line_xml(BX1 + NODE_WIDTH, ROW2_Y + NODE_HEIGHT/2, BX1 + 1.2*U, ROW2_Y + NODE_HEIGHT/2)) # Marriage line
    
    nodes.append(n_elen[0])
    nodes.append(n_jaim[0])
    
    # Elena's Kids
    # Froilan & Victoria
    K1_X = BX1
    K2_X = BX1 + 1.2*U
    
    lines.append(line_xml(BX1 + NODE_WIDTH/2 + 0.6*U, ROW2_Y + NODE_HEIGHT/2, K1_X + NODE_WIDTH/2, ROW3_Y))
    lines.append(line_xml(BX1 + NODE_WIDTH/2 + 0.6*U, ROW2_Y + NODE_HEIGHT/2, K2_X + NODE_WIDTH/2, ROW3_Y))
    
    nodes.append(node_xml(K1_X, ROW3_Y, "Froilán", "Froilan.jpg")[0])
    nodes.append(node_xml(K2_X, ROW3_Y, "Victoria", "Victoria.png")[0])

    # Branch 2: Cristina (Center/Right-ish)
    BX2 = 6 * U # Center
    
    lines.append(line_xml(ORIGIN_X, ORIGIN_Y, BX2 + NODE_WIDTH/2, ROW2_Y))
    
    n_cris = node_xml(BX2, ROW2_Y, "Cristina", "Cristina.jpg", "Infanta")
    n_inak = node_xml(BX2 + 1.2*U, ROW2_Y, "Iñaki", "Inaki.jpg", "Ex-esposo")
    lines.append(line_xml(BX2 + NODE_WIDTH, ROW2_Y + NODE_HEIGHT/2, BX2 + 1.2*U, ROW2_Y + NODE_HEIGHT/2))
    
    nodes.append(n_cris[0])
    nodes.append(n_inak[0])
    
    # Cristina's Kids (4)
    # Juan, Pablo, Miguel, Irene
    # Spread them below
    Start_KX2 = BX2 - 1.5*U
    
    # Manual map for Urdangarin kids filenames
    urdangarin_files = {
        "Juan": "JuanU.png",
        "Pablo": "Pablo.png",
        "Miguel": "Miguel.png",
        "Irene": "Irene.png"
    }
    
    for i, name in enumerate(["Juan", "Pablo", "Miguel", "Irene"]):
        kx = Start_KX2 + (i+1)*1.1*U
        lines.append(line_xml(BX2 + NODE_WIDTH/2 + 0.6*U, ROW2_Y + NODE_HEIGHT/2, kx + NODE_WIDTH/2, ROW3_Y))
        nodes.append(node_xml(kx, ROW3_Y, name, urdangarin_files[name])[0])


    # Branch 3: Felipe (Far Right)
    BX3 = 11 * U
    
    lines.append(line_xml(ORIGIN_X, ORIGIN_Y, BX3 + NODE_WIDTH/2, ROW2_Y))
    
    n_fel = node_xml(BX3, ROW2_Y, "Felipe VI", "Felipe.jpg", "Rey")
    n_let = node_xml(BX3 + 1.2*U, ROW2_Y, "Letizia", "Letizia.jpg", "Reina")
    lines.append(line_xml(BX3 + NODE_WIDTH, ROW2_Y + NODE_HEIGHT/2, BX3 + 1.2*U, ROW2_Y + NODE_HEIGHT/2))
    
    nodes.append(n_fel[0])
    nodes.append(n_let[0])
    
    # Felipe's Kids
    K_F1 = BX3 
    K_F2 = BX3 + 1.2*U
    
    lines.append(line_xml(BX3 + NODE_WIDTH/2 + 0.6*U, ROW2_Y + NODE_HEIGHT/2, K_F1 + NODE_WIDTH/2, ROW3_Y))
    lines.append(line_xml(BX3 + NODE_WIDTH/2 + 0.6*U, ROW2_Y + NODE_HEIGHT/2, K_F2 + NODE_WIDTH/2, ROW3_Y))
    
    nodes.append(node_xml(K_F1, ROW3_Y, "Leonor", "Leonor.JPG", "Princesa")[0])
    nodes.append(node_xml(K_F2, ROW3_Y, "Sofía", "SofiaHija.jpg", "Infanta")[0])


    # --- Assembly ---
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="650" viewBox="0 0 1600 650" style="background-color: white;">\n'
    svg += "<!-- Lines -->\n" + "\n".join(lines) + "\n"
    svg += "<!-- Nodes -->\n" + "\n".join(nodes) + "\n"
    svg += "</svg>"

    with open(OUTPUT_FILE, "w") as f:
        f.write(svg)
    
    print(f"Generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
