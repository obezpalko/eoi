---
description: Rules for processing lesson files in 10-Lecciones/
---
1. **Scope**: Apply this workflow only to files in `10-Lecciones/`.
2. **Metadata**:
   - Filename MUST be `YYYYMMDD Lección [Nombre].md`.
   - Frontmatter MUST include `date: YYYY-MM-DD` and `tags: [lección]`.
3. **Structure**:
   - Single H1 title: `# XXX: [Topic]` where XXX is 3-digit lesson number (001, 002...).
   - Use H2 for sections.
4. **Navigation**:
   - Ensure "Anterior", "Siguiente", and "Deberes" links at the bottom.
5. **Content**:
   - Spanish level A1-A2.
   - Extract new vocabulary to `30-Vocabulario/` files.
6. // turbo
   - Run `python3 80-Tools/fix_links.py` if needed.
