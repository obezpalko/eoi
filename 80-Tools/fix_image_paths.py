#!/usr/bin/env python3
"""
Script to find and fix non-relative image paths in markdown files.
Converts absolute paths like ![[60-Cultura/España vs Hispanoamerica/image.jpg]]
to relative paths like ![[image.jpg]] when the file is already in that directory.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Base directory (repository root)
BASE_DIR = Path(__file__).parent.parent

def find_all_md_files() -> List[Path]:
    """Find all .md files in the repository."""
    md_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip hidden directories and .obsidian
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files

def is_absolute_path(image_ref: str) -> bool:
    """Check if an image reference uses an absolute path (starts with directory name)."""
    # Check if it starts with a numbered directory (10-, 20-, 30-, etc.)
    if re.match(r'^\d{2}-', image_ref):
        return True
    # Check if it contains a slash and starts with a directory name
    if '/' in image_ref and not image_ref.startswith('./') and not image_ref.startswith('../'):
        # Check if it starts with a known directory structure
        parts = image_ref.split('/')
        if len(parts) > 1 and re.match(r'^\d{2}-', parts[0]):
            return True
    return False

def make_relative_path(image_ref: str, md_file: Path) -> str:
    """
    Convert an absolute image path to a relative path.
    For example: 60-Cultura/España vs Hispanoamerica/gafas.jpg -> gafas.jpg
    when md_file is in that directory.
    """
    # Extract just the filename
    filename = Path(image_ref).name
    
    # Check if the image is in the same directory as the md file
    potential_path = md_file.parent / filename
    if potential_path.exists():
        return filename
    
    # Check if it's in a subdirectory
    for subdir in md_file.parent.iterdir():
        if subdir.is_dir():
            potential_path = subdir / filename
            if potential_path.exists():
                # Return relative path from md_file
                relative = os.path.relpath(potential_path, md_file.parent)
                return relative.replace('\\', '/')
    
    # If we can't find it, try to resolve from base directory
    if '/' in image_ref:
        parts = image_ref.split('/')
        # Try to find the image by following the path from base
        base_path = BASE_DIR
        for part in parts:
            base_path = base_path / part
            if base_path.exists() and base_path.is_file():
                # Calculate relative path
                relative = os.path.relpath(base_path, md_file.parent)
                return relative.replace('\\', '/')
    
    # If we can't resolve it, return the filename (might be missing)
    return filename

def fix_image_paths_in_file(md_file: Path) -> Tuple[List[str], List[str], bool]:
    """
    Fix non-relative image paths in a markdown file.
    Returns: (fixed_refs, broken_refs, was_modified)
    """
    try:
        content = md_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return [], [], False
    
    # Pattern for Obsidian image syntax: ![[path/to/image.jpg]]
    pattern = r'!\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    
    fixed_refs = []
    broken_refs = []
    modified = False
    
    for ref in matches:
        if is_absolute_path(ref):
            # Try to make it relative
            relative_ref = make_relative_path(ref, md_file)
            
            # Check if the relative path actually exists
            relative_path = md_file.parent / relative_ref
            if relative_path.exists():
                # Replace in content
                old_ref = f'![[{ref}]]'
                new_ref = f'![[{relative_ref}]]'
                content = content.replace(old_ref, new_ref)
                fixed_refs.append(f"{ref} -> {relative_ref}")
                modified = True
            else:
                broken_refs.append(ref)
    
    if modified:
        md_file.write_text(content, encoding='utf-8')
    
    return fixed_refs, broken_refs, modified

def main():
    print("Finding and fixing non-relative image paths...")
    print("=" * 60)
    
    md_files = find_all_md_files()
    total_fixed = 0
    total_broken = 0
    files_modified = 0
    
    for md_file in sorted(md_files):
        fixed_refs, broken_refs, modified = fix_image_paths_in_file(md_file)
        
        if fixed_refs or broken_refs:
            print(f"\n{md_file.relative_to(BASE_DIR)}:")
            
            if fixed_refs:
                files_modified += 1
                total_fixed += len(fixed_refs)
                for fix in fixed_refs:
                    print(f"  ✓ Fixed: {fix}")
            
            if broken_refs:
                total_broken += len(broken_refs)
                for broken in broken_refs:
                    print(f"  ❌ Broken (image missing): {broken}")
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Files modified: {files_modified}")
    print(f"  Paths fixed: {total_fixed}")
    print(f"  Broken/missing images: {total_broken}")
    print("=" * 60)
    
    if total_broken > 0:
        print(f"\n⚠️  Found {total_broken} missing images that need to be downloaded.")
        print("   Run the download script to fetch these images.")

if __name__ == "__main__":
    main()
