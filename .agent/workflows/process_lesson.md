---
description: Standardize a lesson file, extracting vocabulary, translating notes, and ensuring project structure recommendations are met.
---

1. **Analyze the Request & Context**

   - Identify the target lesson file (usually in `10-Lecciones/`).
   - Read `structure_recommendations.md` to ensure strict adherence to project guidelines.

2. **Standardize Structure & Frontmatter**

   - **Frontmatter**: Ensure the file starts with YAML frontmatter containing:
     - `date`: YYYY-MM-DD (extracted from filename).
     - `tags`: `[lección]` (plus others if relevant).
   - **Headings**: Ensure the file uses a single H1 `# Title` and H2 `## Section` hierarchy.
   - **Title Format**: The H1 title should follow the format `# XXX: [Topic Name]` (e.g., `# 001: Presentación Personal`), where `XXX` is the 3-digit lesson number with leading zeros. Analyze the lesson content to determine the main topic and update the title accordingly.
   - **Links**: Verify that the file ends with navigation links (Previous/Next lesson, Homework).

3. **Process Vocabulary**

   - Read the relevant files in `30-Vocabulario/` (e.g., `Sustantivos.md`, `Verbos básicos.md`, `Adjetivos.md`).
   - Extract new vocabulary definitions from the lesson.
   - **Action**: Add missing words to the correct file and section.
   - **Articles**: For nouns, ensure you add the definite article (**el** or **la**).
   - **Sorting**: Ensure EVERY section in the updated vocabulary files is sorted alphabetically.
   - **Antonyms/Synonyms**: If the lesson introduces new oppositions (e.g., `≠`, `!=`, `opuesto`) or similarities (e.g., `==`, `sinónimo`), update `30-Vocabulario/Temas/Antónimos y Sinónimos.md`.
   - **Images**: If new vocabulary is significant, suggest or run `80-Tools/download_images_universal.py` for those terms.

4. **Content Refinement**

   - **Translation**: Translate any remaining comments or notes (e.g., Russian, English) into simple Spanish (A1-A2).
   - **Correction**: Fix any "improper" words or typos.
   - **Style**: Ensure images are embedded utilizing standard markdown syntax `![[image.jpg]]` or relative paths vs absolute.

5. **Final Validation**

   - Run a quick lint check (check for multiple blank lines, correct header spacing).
   - Ensure all internal links work (relative paths).
