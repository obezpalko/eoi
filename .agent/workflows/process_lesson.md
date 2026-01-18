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
   - **Links**: Verify that the file ends with navigation links (Previous/Next lesson, Homework).

3. **Process Vocabulary**

   - Read `30-Vocabulario/palabras.md`.
   - Extract new vocabulary definitions from the lesson.
   - **Action**: Add missing words to `30-Vocabulario/palabras.md`, ensuring they are placed in the correct category/section.
   - **Sorting**: Ensure EVERY section in `30-Vocabulario/palabras.md` is sorted alphabetically after adding new words.
   - **Images**: If new vocabulary is significant, suggest or run `80-Tools/download_images_universal.py` for those terms.

4. **Content Refinement**

   - **Translation**: Translate any remaining comments or notes (e.g., Russian, English) into simple Spanish (A1-A2).
   - **Correction**: Fix any "improper" words or typos.
   - **Style**: Ensure images are embedded utilizing standard markdown syntax `![[image.jpg]]` or relative paths vs absolute.

5. **Final Validation**

   - Run a quick lint check (check for multiple blank lines, correct header spacing).
   - Ensure all internal links work (relative paths).
