# Quick Start: Lesson Navigation Updater

## What is it?

A Python script that automatically updates navigation links at the bottom of lesson files.

## Quick Usage

### 1. Preview what will change (recommended first step)

```bash
cd /home/alexb/src/github.com/obezpalko/eoi/80-Tools
python update_lesson_navigation.py --dry-run --verbose
```

### 2. Update all lesson files

```bash
cd /home/alexb/src/github.com/obezpalko/eoi/80-Tools
python update_lesson_navigation.py
```

## What it does

For each lesson in `10-Lecciones/`, it creates or updates a navigation section like this:

```markdown
---

**Navegación:**
[[20260114 Lección veintisiete|← Lección anterior]] | [[../index|Inicio]] | [[../40-Deberes/20260119 Lección veintiocho|Deberes →]]
```

Where:

- **← Lección anterior** = Link to previous lesson
- **Inicio** = Link to home page
- **Deberes →** = Link to homework (dated with next lesson's date)

## When to use it

- After adding a new lesson
- After renaming lesson files
- When homework files are added/renamed
- To fix broken navigation links

## Full Documentation

See `README_navigation_updater.md` for complete documentation.
