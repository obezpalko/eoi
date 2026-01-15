# Recomendaciones de Estructura del Proyecto

Este documento describe las mejores prácticas específicas para mantener el proyecto EOI organizado.

---

## 1. Configuración Específica

### Obsidian
- Configuración de enlaces: **"Relative path to file"** (ruta relativa desde el archivo actual)

### Inteligencia Artificial
- Contenido en **español (Nivel A1-A2)**
- Imágenes **sin texto superpuesto**
- Herramienta: `80-Tools/download_images_universal.py`

---

## 2. Estructura de Lecciones

- Formato de nombres: `YYYYMMDD Lección [nombre].md`
- Navegación: Enlaces a lección anterior/siguiente y página de deberes al final
- Frontmatter con fecha extraída del nombre del archivo

---

## 3. Convenciones de Nombrado

### Numeración de Carpetas
- Prefijos numéricos con espacios: `10-`, `20-`, `30-`, `40-`, `50-`, `60-`, `80-`
- Permite futuras expansiones sin renombrar

### Formato de Nombres
- **Archivos markdown:** Espacios permitidos (`Siempre Plural.md`)
- **Scripts:** `snake_case` (`download_images_universal.py`)
- **Imágenes:** `snake_case` sin espacios (`gafas_de_sol.jpg`)

---

## 4. Gestión de Imágenes

### Ubicación
Carpeta con el mismo nombre que el archivo markdown:

```
30-Vocabulario/Temas/
├── Ropa y Accesorios.md
└── Ropa y Accesorios/
    └── pantalones.jpg
```

Referencias: `![[Ropa y Accesorios/pantalones.jpg]]`

### Especificaciones
- **Tamaño:** max 256x256px, preservar aspecto original
- **Formato:** JPG (fotos), SVG (gráficos vectoriales)
- **Calidad:** 85% JPG
- **Sin texto superpuesto**

### Herramienta de Descarga
```bash
python3 80-Tools/download_images_universal.py \
  --csv archivo.csv \
  --output "ruta/destino" \
  --size 256x256 \
  --quality 85 \
  --force
```

---

## 5. Notas de Carpeta (Folder Notes)

Nota con el mismo nombre que la carpeta al mismo nivel:

```
30-Vocabulario/Temas/
├── Siempre Plural.md             ← Nota índice
└── Siempre Plural/               ← Carpeta con imágenes
```

Compatible con Obsidian y Quartz.

---

## 6. Scripts (80-Tools/)

Principios:
- Genéricos con argumentos (sin rutas hardcoded)
- Documentados con ejemplos de uso

Scripts principales:
- `download_images_universal.py` - Descarga imágenes desde DuckDuckGo
- `fix_links.py` - Corrige enlaces relativos
- `add_frontmatter.py` - Añade metadatos YAML

---

## 7. Frontmatter

```yaml
---
date: YYYY-MM-DD
tags: [lección, español, vocabulario]
---
```

Etiquetas por carpeta: `lección`, `gramática`, `vocabulario`, `tema`, `verbo`, `cultura`, `deberes`

---

## 8. Quartz (Sitio Estático)

**Configuración:** `quartz.config.ts`
- `markdownLinkResolution: "relative"`
- Ignorados: `90-Archivos`, `99-Exports`, `structure_recommendations.md`

**Despliegue:** GitHub Actions → `https://obezpalko.github.io/eoi/`

**Página de inicio:** `index.md` con `[component: FolderContent]`

---

## 9. Puntos Clave

- Nivel español: A1-A2
- Tablas para vocabulario con ejemplos contextuales
- Rutas relativas en todos los enlaces
- Imágenes sin texto, max 256x256px, aspecto preservado
- Frontmatter con fecha y tags en todos los archivos
- Folder notes para temas principales

