#!/usr/bin/env python3
"""Generate SVG color swatches for the Colores vocabulary page."""

import os

# Define all colors with their hex codes
colors = {
    # Colores Básicos
    "rojo": "#E63946",
    "naranja": "#FF7F11",
    "morado": "#6A0DAD",
    "violeta": "#8F00FF",
    "verde": "#2ECC71",
    "rosa_fucsia": "#FF2D95",
    "azul": "#1D4ED8",
    "azul_celeste": "#87CEEB",
    "azul_marino": "#001F54",
    "azul_claro": "#7CC6FE",
    "negro": "#000000",
    "blanco": "#FFFFFF",
    "gris": "#A8A8A8",
    "marron": "#7B3F00",
    "lila": "#C8A2C8",
    # Colores Adicionales
    "rosa": "#FFC0CB",
    "melocoton": "#FFB347",
    "dorado": "#FFD700",
    "plateado": "#C0C0C0",
    "cobre": "#B87333",
    "caramelo": "#9A6324",
    "arena": "#F4A460",
    "beige": "#FAEBD7",
    "crema": "#F5F5DC",
    "marfil": "#FFE4C4",
    # Tonos de Verde
    "verde_bosque": "#228B22",
    "verde_lima": "#ADFF2F",
    "verde_brillante": "#32CD32",
    "turquesa": "#20B2AA",
    "turquesa_claro": "#40E0D0",
    # Tonos de Rojo
    "granate": "#800000",
    "rojo_anaranjado": "#FF4500",
    "carmesi": "#DC143C",
    # Tonos de Morado/Púrpura
    "purpura": "#9932CC",
    "rosa_pastel": "#FFC1CC",
    # Tonos de Azul/Gris
    "azul_acero": "#4682B4",
    "gris_azulado": "#708090",
}

# SVG template for color swatch
svg_template = '''<svg width="60" height="30" xmlns="http://www.w3.org/2000/svg">
  <rect width="60" height="30" fill="{color}" stroke="#333" stroke-width="1"/>
</svg>'''

# Output directory
output_dir = "/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/Colores/swatches"

# Generate SVG files
for name, color in colors.items():
    svg_content = svg_template.format(color=color)
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, 'w') as f:
        f.write(svg_content)
    print(f"Created: {name}.svg")

print(f"\nTotal: {len(colors)} SVG files created in {output_dir}")
