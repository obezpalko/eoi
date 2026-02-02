---
description: Rules for vocabulary files in 30-Vocabulario/
---
1. **Scope**: Apply to files in `30-Vocabulario/` and its subdirectories.
2. **Metadata**:
   - Tags: `[vocabulario, español]`.
3. **Noun Rules**:
   - ALWAYS include definite articles (`el`, `la`, `los`, `las`).
4. **Table Structure**:
   - MUST have standard columns: `Palabra`, `Definición/Descripción`, `Ejemplo`, `Imagen`.
5. **Alphabetical Order**:
   - ALL tables and lists MUST be sorted alphabetically.
6. **Images**:
   - Use `![[Subfolder/image.jpg]]` syntax.
   - // turbo
     Run `python3 80-Tools/download_images_universal.py --output "30-Vocabulario/Temas/Topic" --items "word:query"` for new entries.
7. **Slang and Vulgarisms**:
   - Colloquial, informal, or vulgar terms MUST be added to `30-Vocabulario/Temas/Jerga y Expresiones Vulgares.md` in addition to general lists.
   - For easily confused words (e.g., `cojín` vs `cojones`), highlight the phonetic comparison in the table.
8. **Folder Notes**:
   - If a topic file exists (e.g., `Profesiones.md`), related images go in `Profesiones/`.
