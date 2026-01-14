#!/usr/bin/env python3
"""
Script to download missing images identified by check_image_links.py.
Extracts broken image references and downloads them using download_images_universal.py
"""

import subprocess
import sys
from pathlib import Path

# Import the check_image_links functions
sys.path.insert(0, str(Path(__file__).parent))
from check_image_links import check_image_links, find_all_md_files, extract_image_references, resolve_image_path

BASE_DIR = Path(__file__).parent.parent

def find_missing_images() -> dict:
    """
    Find all missing images grouped by markdown file.
    Returns: {md_file: [list of missing image refs]}
    """
    link_results, _ = check_image_links()
    missing_by_file = {}
    
    for md_file, refs in link_results.items():
        missing = []
        for ref, exists, resolved in refs:
            if not exists:
                missing.append(ref)
        if missing:
            missing_by_file[md_file] = missing
    
    return missing_by_file

def create_download_commands(missing_by_file: dict):
    """
    Create download commands for missing images.
    Groups by output directory (same as md file's directory).
    """
    commands = []
    
    for md_file, missing_refs in missing_by_file.items():
        output_dir = md_file.parent
        
        # Extract filenames and create search queries
        items = []
        for ref in missing_refs:
            # Get filename without extension for search query
            filename = Path(ref).stem
            # Create a search query from the filename
            # Replace underscores/hyphens with spaces
            query = filename.replace('_', ' ').replace('-', ' ')
            items.append(f"{filename}:{query}")
        
        if items:
            cmd = [
                "python3",
                str(BASE_DIR / "80-Tools" / "download_images_universal.py"),
                "--output", str(output_dir),
                "--items"
            ] + items
            
            commands.append({
                'md_file': md_file,
                'output_dir': output_dir,
                'command': cmd,
                'items': items
            })
    
    return commands

def main():
    print("Finding missing images...")
    print("=" * 60)
    
    missing_by_file = find_missing_images()
    
    if not missing_by_file:
        print("✓ No missing images found!")
        return
    
    print(f"\nFound missing images in {len(missing_by_file)} file(s):")
    for md_file, missing in missing_by_file.items():
        print(f"\n  {md_file.relative_to(BASE_DIR)}:")
        for ref in missing:
            print(f"    - {ref}")
    
    print("\n" + "=" * 60)
    print("Creating download commands...")
    print("=" * 60)
    
    commands = create_download_commands(missing_by_file)
    
    for cmd_info in commands:
        print(f"\n📁 {cmd_info['md_file'].relative_to(BASE_DIR)}")
        print(f"   Output: {cmd_info['output_dir'].relative_to(BASE_DIR)}")
        print(f"   Command:")
        print(f"   {' '.join(cmd_info['command'])}")
        
        # Ask user if they want to download
        response = input(f"\n   Download {len(cmd_info['items'])} images? (y/n): ").strip().lower()
        if response == 'y':
            print(f"   Downloading...")
            try:
                result = subprocess.run(cmd_info['command'], cwd=BASE_DIR, check=True)
                print(f"   ✓ Download completed!")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   Skipped.")

if __name__ == "__main__":
    main()
