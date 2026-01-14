#!/usr/bin/env python3
"""
Script to check and fix image links in .md files and find unused images.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List, Tuple

# Base directory (repository root)
BASE_DIR = Path(__file__).parent.parent

# Image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp', '.jpeg'}

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

def find_all_image_files() -> Set[Path]:
    """Find all image files in the repository."""
    image_files = set()
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip hidden directories and .obsidian
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                image_files.add(Path(root) / file)
    return image_files

def extract_image_references(md_file: Path) -> List[str]:
    """Extract all image references from a markdown file."""
    try:
        content = md_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return []
    
    # Pattern for Obsidian image syntax: ![[path/to/image.jpg]]
    pattern = r'!\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return matches

def resolve_image_path(image_ref: str, md_file: Path) -> Path:
    """
    Resolve an image reference to an absolute path.
    Obsidian resolves paths relative to the .md file location.
    """
    # Remove any leading/trailing whitespace
    image_ref = image_ref.strip()
    
    # If it's an absolute path (starts with a directory name)
    if '/' in image_ref:
        # Try relative to md file first
        relative_path = md_file.parent / image_ref
        if relative_path.exists():
            return relative_path.resolve()
        
        # Try from base directory
        base_path = BASE_DIR / image_ref
        if base_path.exists():
            return base_path.resolve()
    
    # Simple filename - relative to md file
    relative_path = md_file.parent / image_ref
    if relative_path.exists():
        return relative_path.resolve()
    
    # Try in subdirectories of md file's parent
    for subdir in md_file.parent.iterdir():
        if subdir.is_dir():
            potential_path = subdir / image_ref
            if potential_path.exists():
                return potential_path.resolve()
    
    # Return None if not found (will be handled by caller)
    return None

def check_image_links() -> Tuple[Dict[Path, List[Tuple[str, bool, Path]]], Set[str]]:
    """
    Check all image links in .md files.
    Returns: (file -> [(ref, exists, resolved_path), ...], all_referenced_images)
    """
    md_files = find_all_md_files()
    results = defaultdict(list)
    all_referenced = set()
    
    for md_file in md_files:
        refs = extract_image_references(md_file)
        for ref in refs:
            resolved = resolve_image_path(ref, md_file)
            exists = resolved is not None and resolved.exists()
            results[md_file].append((ref, exists, resolved))
            if exists:
                all_referenced.add(str(resolved))
    
    return results, all_referenced

def find_unused_images() -> List[Path]:
    """Find images that are not referenced in any .md file."""
    _, referenced_images = check_image_links()
    all_images = find_all_image_files()
    
    # Convert referenced images to Path objects for comparison
    referenced_paths = {Path(img) for img in referenced_images}
    
    unused = []
    for img in all_images:
        if img.resolve() not in {p.resolve() for p in referenced_paths}:
            unused.append(img)
    
    return sorted(unused)

def fix_broken_links(md_file: Path, broken_refs: List[Tuple[str, bool, Path]]) -> bool:
    """Try to fix broken image links by searching for similar filenames."""
    content = md_file.read_text(encoding='utf-8')
    modified = False
    
    for ref, exists, resolved in broken_refs:
        if exists:
            continue  # Not broken
        
        # Try to find the image by filename
        filename = Path(ref).name
        all_images = find_all_image_files()
        
        # Look for exact filename match
        matches = [img for img in all_images if img.name == filename]
        
        if matches:
            # Use the first match, calculate relative path
            match = matches[0]
            try:
                relative_path = os.path.relpath(match, md_file.parent)
                # Use forward slashes for Obsidian
                relative_path = relative_path.replace('\\', '/')
                
                # Replace the broken reference
                old_ref = f'![[{ref}]]'
                new_ref = f'![[{relative_path}]]'
                content = content.replace(old_ref, new_ref)
                modified = True
                print(f"  Fixed: {ref} -> {relative_path}")
            except Exception as e:
                print(f"  Could not fix {ref}: {e}")
    
    if modified:
        md_file.write_text(content, encoding='utf-8')
    
    return modified

def main():
    print("Checking image links in .md files...")
    print("=" * 60)
    
    # Check all links
    link_results, referenced_images = check_image_links()
    
    broken_count = 0
    fixed_count = 0
    
    print("\nBroken image links:")
    print("-" * 60)
    
    for md_file, refs in sorted(link_results.items()):
        broken = [(ref, exists, resolved) for ref, exists, resolved in refs if not exists]
        if broken:
            broken_count += len(broken)
            print(f"\n{md_file.relative_to(BASE_DIR)}:")
            for ref, exists, resolved in broken:
                print(f"  ❌ {ref}")
            
            # Try to fix broken links
            if fix_broken_links(md_file, broken):
                fixed_count += len(broken)
    
    if broken_count == 0:
        print("  ✓ No broken links found!")
    
    # Find unused images
    print("\n" + "=" * 60)
    print("Finding unused images...")
    print("-" * 60)
    
    unused_images = find_unused_images()
    
    if unused_images:
        print(f"\nFound {len(unused_images)} unused images:")
        for img in unused_images:
            print(f"  {img.relative_to(BASE_DIR)}")
        
        # Write to file
        unused_file = BASE_DIR / "80-Tools" / "unused_images.txt"
        with open(unused_file, 'w', encoding='utf-8') as f:
            f.write("Unused Images\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total: {len(unused_images)}\n\n")
            for img in unused_images:
                f.write(f"{img.relative_to(BASE_DIR)}\n")
        
        print(f"\n✓ List saved to: {unused_file.relative_to(BASE_DIR)}")
    else:
        print("\n  ✓ No unused images found!")
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Broken links found: {broken_count}")
    print(f"  Links fixed: {fixed_count}")
    print(f"  Unused images: {len(unused_images)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
