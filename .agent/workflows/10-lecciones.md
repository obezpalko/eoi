---
description: Rules for processing lesson files in 10-Lecciones/1A2/ and 10-Lecciones/2A2/
---

1. **Scope**: Apply this workflow only to files in `10-Lecciones/1A2/` and `10-Lecciones/2A2/`.
2. **Metadata**:
   - Filename MUST be `YYYYMMDD Lección [Nombre].md`.
   - Frontmatter MUST include `date: YYYY-MM-DD` and `tags: [lección]`.
3. **Structure**:
   - Single H1 title: `# XXX: [Topic]` where XXX is 3-digit lesson number (001, 002...).
   - Use H2 for sections.
4. **Navigation**:
   - Ensure "Anterior", "Siguiente", and "Deberes" links at the bottom.
   - 1A2: homework is a separate note in `10-Lecciones/1A2/Deberes/`. 2A2: homework is a `## Deberes` section in the lesson, linked as `[[#Deberes|📝 Deberes]]`.
   - `80-Tools/update_lesson_navigation.py` (pre-commit hook) maintains the footer for both folders.
   - New 2A2 lessons start from `90-Archivos/Plantillas/Lección 2A2.md`.
5. **Content**:
   - Spanish level A1-A2.
   - Extract new vocabulary to `30-Vocabulario/` files.
6. **Project**:
   - Use: Use `@[.agent/workflows/process_lesson.md]` as additional rules.
7. // turbo
   - Run `python3 80-Tools/fix_links.py` if needed.
