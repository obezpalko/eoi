#!/usr/bin/env python3
"""
Lesson Navigation Updater

This script verifies and updates the navigation section at the bottom of lesson files.
The navigation section contains links to:
- Previous lesson
- Next lesson  
- Homework (dated with the next lesson's date)

Usage:
    python update_lesson_navigation.py [--dry-run] [--verbose]
    
Options:
    --dry-run    Show what would be changed without modifying files
    --verbose    Show detailed information about processing
"""

import re
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional


class LessonFile:
    """Represents a lesson file with its metadata."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filename = filepath.name
        
        # Extract date and lesson name from filename
        # Format: YYYYMMDD Lección <name>.md
        match = re.match(r'(\d{8})\s+Lección\s+(.+)\.md', self.filename)
        if match:
            self.date_str = match.group(1)
            self.lesson_name = match.group(2)
            # Skip template file before parsing date
            if self.date_str != '00000000':
                self.date = datetime.strptime(self.date_str, '%Y%m%d')
            else:
                self.date = None
        else:
            self.date_str = None
            self.lesson_name = None
            self.date = None
    
    def is_valid_lesson(self) -> bool:
        """Check if this is a valid lesson file (not template)."""
        return (self.date_str is not None and 
                self.lesson_name is not None and
                self.date_str != '00000000')
    
    def __repr__(self):
        return f"LessonFile({self.filename})"
    
    def __lt__(self, other):
        """Compare lessons by date for sorting."""
        if self.date and other.date and self.date != other.date:
            return self.date < other.date
        return self.filename < other.filename


def find_lesson_files(lessons_dir: Path) -> List[LessonFile]:
    """Find all valid lesson files in the directory."""
    lesson_files = []
    
    for filepath in lessons_dir.glob('*.md'):
        lesson = LessonFile(filepath)
        if lesson.is_valid_lesson():
            lesson_files.append(lesson)
    
    # Sort by date
    lesson_files.sort()
    
    return lesson_files




def read_file_content(filepath: Path) -> str:
    """Read file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file_content(filepath: Path, content: str):
    """Write content to file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_navigation_section(content: str) -> Tuple[Optional[str], int, int]:
    """
    Extract the navigation section from the content.
    
    Returns:
        Tuple of (navigation_text, start_pos, end_pos)
        If no navigation section found, returns (None, -1, -1)
    """
    # Look for the navigation section pattern
    # It should be after --- and contain **Navegación:**
    pattern = r'---\s*\n\s*\*\*Navegación:\*\*\s*\n(.+?)(?:\n|$)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip(), match.start(), match.end()
    
    return None, -1, -1


def build_navigation_section(prev_lesson: Optional[LessonFile], 
                            next_lesson: Optional[LessonFile],
                            homework_link: Optional[str]) -> str:
    """
    Build the navigation section text.
    
    Args:
        prev_lesson: Previous lesson file or None
        next_lesson: Next lesson file or None  
        homework_link: Link to homework file or None
        
    Returns:
        The formatted navigation section
    """
    parts = []
    
    # Previous lesson link
    if prev_lesson:
        parts.append(f"[[{prev_lesson.filename[:-3]}|⬅️ Lección anterior]]")
    else:
        parts.append("⬅️ Lección anterior")
    
    # Home link
    parts.append("[[../index|🏠 Inicio]]")
    
    # Homework link
    if homework_link:
        parts.append(f"[[{homework_link[:-3]}|📝 Deberes]]")
    else:
        parts.append("📝 Deberes")
    
    # Next lesson link
    if next_lesson:
        parts.append(f"[[{next_lesson.filename[:-3]}|Lección siguiente ➡️]]")
    else:
        parts.append("Lección siguiente ➡️")
    
    navigation = " | ".join(parts)
    
    return f"---\n\n**Navegación:**\n{navigation}\n"


def update_lesson_navigation(lesson: LessonFile, 
                            prev_lesson: Optional[LessonFile],
                            next_lesson: Optional[LessonFile],
                            homework_dir: Path,
                            dry_run: bool = False,
                            verbose: bool = False) -> bool:
    """
    Update the navigation section for a lesson file.
    
    Returns:
        True if changes were made (or would be made in dry-run), False otherwise
    """
    content = read_file_content(lesson.filepath)
    
    # The homework for the current lesson is expected to be in a file
    # with the same name as the NEXT lesson, but in the 40-Deberes folder.
    if next_lesson:
        homework_link = f"../40-Deberes/{next_lesson.filename}"
    else:
        homework_link = None
    
    # Build the expected navigation section
    expected_nav = build_navigation_section(prev_lesson, next_lesson, homework_link)
    
    # Extract current navigation section
    current_nav, start_pos, end_pos = extract_navigation_section(content)
    
    if current_nav is None:
        # No navigation section found, add it at the end
        if verbose:
            print(f"  ⚠️  No navigation section found in {lesson.filename}")
        
        # Make sure content ends with a newline
        if not content.endswith('\n'):
            content += '\n'
        
        new_content = content + expected_nav
        
        if not dry_run:
            write_file_content(lesson.filepath, new_content)
        
        if verbose or dry_run:
            print(f"  ➕ Would add navigation section" if dry_run else f"  ✅ Added navigation section")
        
        return True
    
    else:
        # Check if navigation needs updating
        current_full = content[start_pos:end_pos]
        
        if current_full.strip() != expected_nav.strip():
            if verbose:
                print(f"  ⚠️  Navigation section needs updating in {lesson.filename}")
                if verbose:
                    print(f"     Current:  {current_nav}")
                    print(f"     Expected: {expected_nav.split('**Navegación:**')[1].strip()}")
            
            new_content = content[:start_pos] + expected_nav + content[end_pos:]
            
            if not dry_run:
                write_file_content(lesson.filepath, new_content)
            
            if verbose or dry_run:
                print(f"  🔄 Would update navigation" if dry_run else f"  ✅ Updated navigation")
            
            return True
        else:
            if verbose:
                print(f"  ✓ Navigation is correct in {lesson.filename}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Update navigation sections in lesson files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check what would be changed
  python update_lesson_navigation.py --dry-run --verbose
  
  # Update all lesson files
  python update_lesson_navigation.py
  
  # Update with detailed output
  python update_lesson_navigation.py --verbose
        """
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information about processing')
    
    args = parser.parse_args()
    
    # Determine project root (script is in 80-Tools)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    lessons_dir = project_root / '10-Lecciones'
    homework_dir = project_root / '40-Deberes'
    
    if not lessons_dir.exists():
        print(f"❌ Error: Lessons directory not found: {lessons_dir}")
        return 1
    
    if not homework_dir.exists():
        print(f"⚠️  Warning: Homework directory not found: {homework_dir}")
    
    print(f"📚 Finding lesson files in {lessons_dir}")
    lesson_files = find_lesson_files(lessons_dir)
    
    if not lesson_files:
        print("❌ No valid lesson files found")
        return 1
    
    print(f"✓ Found {len(lesson_files)} lesson files")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified\n")
    
    changes_made = 0
    
    for i, lesson in enumerate(lesson_files):
        prev_lesson = lesson_files[i - 1] if i > 0 else None
        next_lesson = lesson_files[i + 1] if i < len(lesson_files) - 1 else None
        
        if args.verbose:
            print(f"\n📄 Processing: {lesson.filename}")
        
        if update_lesson_navigation(lesson, prev_lesson, next_lesson, 
                                   homework_dir, args.dry_run, args.verbose):
            changes_made += 1
    
    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"🔍 {changes_made} file(s) would be updated")
    else:
        print(f"✅ Updated {changes_made} file(s)")
    print(f"{'=' * 60}")
    
    return 0


if __name__ == '__main__':
    exit(main())
