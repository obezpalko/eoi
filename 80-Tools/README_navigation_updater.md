# Lesson Navigation Updater

This tool automatically verifies and updates the navigation section at the bottom of lesson files in the `10-Lecciones` directory.

## What it does

The navigation section provides links to:

- **Previous lesson**: Link to the previous lesson file
- **Home**: Link to the main index
- **Homework**: Link to the homework file for the next lesson (dated with the next lesson's date)

## Navigation Format

The script ensures each lesson file ends with a navigation section like this:

```markdown
---

**Navegación:**
[[20260114 Lección veintisiete|← Lección anterior]] | [[../index|Inicio]] | [[../40-Deberes/20260121 Lección veintiocho|Deberes →]]
```

## Usage

### Basic Usage

```bash
# Navigate to the tools directory
cd /home/alexb/src/github.com/obezpalko/eoi/80-Tools

# Update all lesson navigation sections
python update_lesson_navigation.py
```

### Dry Run (Preview Changes)

To see what would be changed without modifying any files:

```bash
python update_lesson_navigation.py --dry-run
```

### Verbose Mode

To see detailed information about each file being processed:

```bash
python update_lesson_navigation.py --verbose
```

### Combine Options

```bash
# See detailed preview of all changes
python update_lesson_navigation.py --dry-run --verbose
```

## How it Works

1. **Scans** the `10-Lecciones` directory for all lesson files
2. **Sorts** lessons by date (extracted from filename: `YYYYMMDD Lección <name>.md`)
3. **For each lesson**:
   - Determines the previous and next lessons
   - Finds the corresponding homework file in `40-Deberes`
   - Checks if the navigation section exists and is correct
   - Updates or adds the navigation section if needed

## Output

The script provides clear feedback:

- ✓ Navigation is correct (verbose mode only)
- ⚠️  No navigation section found
- ➕ Added navigation section
- 🔄 Updated navigation section
- ✅ Final summary of changes

## Examples

### Example 1: Check what needs updating

```bash
python update_lesson_navigation.py --dry-run --verbose
```

Output:

```
📚 Finding lesson files in /home/alexb/src/github.com/obezpalko/eoi/10-Lecciones
✓ Found 29 lesson files

🔍 DRY RUN MODE - No files will be modified

📄 Processing: 20250929 Lección uno.md
  ✓ Navigation is correct in 20250929 Lección uno.md

📄 Processing: 20251001 Lección dos.md
  ⚠️  Navigation section needs updating in 20251001 Lección dos.md
  🔄 Would update navigation

...

============================================================
🔍 3 file(s) would be updated
============================================================
```

### Example 2: Update all files

```bash
python update_lesson_navigation.py
```

Output:

```
📚 Finding lesson files in /home/alexb/src/github.com/obezpalko/eoi/10-Lecciones
✓ Found 29 lesson files

============================================================
✅ Updated 3 file(s)
============================================================
```

## File Requirements

The script expects:

- Lesson files in format: `YYYYMMDD Lección <name>.md`
- Lesson files located in `10-Lecciones/` directory
- Homework files located in `40-Deberes/` directory
- Homework files named: `YYYYMMDD Lección <name>.md` (matching lesson date)

## Notes

- The script skips the template file (`00000000 Lección template.md`)
- If a homework file is not found, the script will still create a navigation link (it may point to a non-existent file)
- The script preserves all other content in the lesson files
- Navigation sections are always added at the end of the file after a `---` separator

## Troubleshooting

**Problem**: Script says "No valid lesson files found"

- **Solution**: Make sure you're running the script from the `80-Tools` directory and that lesson files follow the naming convention

**Problem**: Navigation links are incorrect

- **Solution**: Check that homework files exist in `40-Deberes` with matching dates

**Problem**: Script doesn't update a file

- **Solution**: Run with `--verbose` to see why the file was skipped
