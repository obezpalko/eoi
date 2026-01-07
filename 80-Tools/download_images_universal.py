#!/usr/bin/env python3
"""
Universal Image Downloader using DuckDuckGo Image Search

Usage:
    # From CSV file
    python3 download_images_universal.py --csv images.csv --output ./output

    # From JSON file
    python3 download_images_universal.py --json images.json --output ./output

    # From command line
    python3 download_images_universal.py --output ./output --items "car:red car" "house:blue house"

    # From Markdown file (auto-detect image links)
    python3 download_images_universal.py --md vocab.md --output ./output

CSV Format:
    filename,search_query
    car,red sports car
    house,blue house

JSON Format:
    [
        {"filename": "car", "query": "red sports car"},
        {"filename": "house", "query": "blue house"}
    ]
"""

import os
import sys
import json
import csv
import argparse
import time
import re
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# Try to import DuckDuckGo library (handle both versions)
try:
    from ddgs import DDGS
    DDG_VERSION = "ddgs"
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDG_VERSION = "duckduckgo_search"
    except ImportError:
        print("ERROR: Please install duckduckgo_search:")
        print("  pip install duckduckgo-search")
        sys.exit(1)


def search_ddg_images(query, max_results=5, safesearch='moderate', size='Medium'):
    """
    Search DuckDuckGo for images.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        safesearch: 'on', 'moderate', or 'off'
        size: 'Small', 'Medium', 'Large', or None
    
    Returns:
        List of image URLs
    """
    try:
        print(f"    Searching DDG for: '{query}'...")
        
        if DDG_VERSION == "duckduckgo_search":
            with DDGS() as ddgs:
                results = list(ddgs.images(
                    keywords=query,
                    max_results=max_results,
                    safesearch=safesearch,
                    size=size
                ))
        else:
            # ddgs library uses positional argument for query
            ddgs = DDGS()
            results = list(ddgs.images(
                query,
                max_results=max_results,
                safesearch=safesearch,
                size=size
            ))
        
        urls = []
        for result in results:
            url = result.get('image')
            if url and any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                urls.append(url)
        
        if urls:
            print(f"    Found {len(urls)} images")
        else:
            print(f"    No images found")
        
        return urls
        
    except Exception as e:
        print(f"    ✗ Error searching: {e}")
        return []


def download_and_resize_image(url, output_path, max_size=(512, 512), quality=85):
    """
    Download image from URL and resize it.
    
    Args:
        url: Image URL
        output_path: Path to save the image
        max_size: Maximum size as (width, height) tuple
        quality: JPEG quality (1-100)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Open image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary (handle transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize while maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save as JPEG
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return True
        
    except Exception as e:
        print(f"    ✗ Error downloading/resizing: {e}")
        return False


def load_items_from_csv(csv_file):
    """Load image items from CSV file."""
    items = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'filename' in row and 'query' in row:
                items.append({
                    'filename': row['filename'].strip(),
                    'query': row['query'].strip()
                })
            elif 'filename' in row and 'search_query' in row:
                items.append({
                    'filename': row['filename'].strip(),
                    'query': row['search_query'].strip()
                })
    return items


def load_items_from_json(json_file):
    """Load image items from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = []
    for item in data:
        if 'filename' in item and 'query' in item:
            items.append({
                'filename': item['filename'].strip(),
                'query': item['query'].strip()
            })
    return items


def load_items_from_markdown(md_file, output_dir):
    """
    Load image items from Markdown file.
    Searches for image links like ![[path/filename.jpg]] and extracts search terms.
    """
    items = []
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.splitlines()
    
    # Try to parse table rows first (better quality)
    for line in lines:
        if '![[' in line and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            
            # Find the word/term (usually in bold in first columns)
            word_match = None
            description = ""
            
            for i, part in enumerate(parts[1:], 1):  # Skip empty first part
                if not word_match:
                    match = re.search(r'\*\*(.*?)\*\*', part)
                    if match:
                        word_match = match.group(1).strip()
                elif i < len(parts) - 2 and not re.search(r'!\[\[', part):
                    # This might be a description
                    description = part.strip()
            
            # Find image link
            link_match = re.search(r'!\[\[(.*?)\]\]', line)
            
            if link_match and word_match:
                raw_link = link_match.group(1)
                clean_link = raw_link.split('|')[0]
                filename = os.path.basename(clean_link)
                
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    stem = os.path.splitext(filename)[0]
                    
                    # Clean the word (remove articles)
                    query_base = word_match
                    for art in ["el ", "la ", "los ", "las ", "un ", "una ", "unos ", "unas "]:
                        if query_base.lower().startswith(art):
                            query_base = query_base[len(art):]
                            break
                    
                    # Combine word and description for better results
                    if description:
                        final_query = f"{query_base} {description}"
                    else:
                        final_query = query_base
                    
                    items.append({
                        'filename': stem,
                        'query': final_query
                    })
    
    # Fallback: find any image links not yet processed
    all_links = re.findall(r'!\[\[(.*?)\]\]', content)
    existing_filenames = {item['filename'] for item in items}
    
    for raw_link in all_links:
        clean_link = raw_link.split('|')[0]
        filename = os.path.basename(clean_link)
        
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            stem = os.path.splitext(filename)[0]
            
            if stem not in existing_filenames:
                # Use filename as search query
                query = stem.replace('_', ' ').replace('-', ' ')
                items.append({
                    'filename': stem,
                    'query': query
                })
    
    return items


def load_items_from_args(items_args):
    """Load image items from command line arguments."""
    items = []
    for item in items_args:
        if ':' in item:
            filename, query = item.split(':', 1)
            items.append({
                'filename': filename.strip(),
                'query': query.strip()
            })
        else:
            # Use the same string for both filename and query
            items.append({
                'filename': item.strip(),
                'query': item.strip()
            })
    return items


def main():
    parser = argparse.ArgumentParser(
        description='Universal Image Downloader using DuckDuckGo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Input sources (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--csv', help='CSV file with filename,query columns')
    input_group.add_argument('--json', help='JSON file with array of {filename, query} objects')
    input_group.add_argument('--md', help='Markdown file to extract image links from')
    input_group.add_argument('--items', nargs='+', help='Items as "filename:query" pairs')
    
    # Output settings
    parser.add_argument('--output', '-o', required=True, help='Output directory for images')
    parser.add_argument('--size', default='512x512', help='Max image size (e.g., 512x512, 256x256)')
    parser.add_argument('--quality', type=int, default=85, help='JPEG quality (1-100, default: 85)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between downloads in seconds (default: 1.0)')
    parser.add_argument('--max-results', type=int, default=5, help='Max search results to try per image (default: 5)')
    parser.add_argument('--force', action='store_true', help='Re-download existing images')
    parser.add_argument('--extension', default='jpg', choices=['jpg', 'jpeg', 'png'], help='Output file extension (default: jpg)')
    
    args = parser.parse_args()
    
    # Parse size
    try:
        width, height = map(int, args.size.lower().split('x'))
        max_size = (width, height)
    except:
        print(f"ERROR: Invalid size format '{args.size}'. Use format like '512x512'")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load items from specified source
    print("=" * 70)
    print("Universal Image Downloader")
    print("=" * 70)
    
    items = []
    if args.csv:
        print(f"\nLoading from CSV: {args.csv}")
        items = load_items_from_csv(args.csv)
    elif args.json:
        print(f"\nLoading from JSON: {args.json}")
        items = load_items_from_json(args.json)
    elif args.md:
        print(f"\nLoading from Markdown: {args.md}")
        items = load_items_from_markdown(args.md, output_dir)
    elif args.items:
        print(f"\nLoading from command line arguments")
        items = load_items_from_args(args.items)
    
    if not items:
        print("ERROR: No items found to process!")
        sys.exit(1)
    
    print(f"Found {len(items)} items to process\n")
    
    # Process each item
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for i, item in enumerate(items, 1):
        filename = item['filename']
        query = item['query']
        
        # Ensure safe filename
        safe_filename = re.sub(r'[^\w\s-]', '', filename)
        safe_filename = re.sub(r'[-\s]+', '_', safe_filename)
        output_file = output_dir / f"{safe_filename}.{args.extension}"
        
        print(f"[{i}/{len(items)}] {filename}")
        print(f"  Query: '{query}'")
        
        # Check if file exists
        if output_file.exists() and not args.force:
            print(f"  ⊙ Already exists: {output_file.name}")
            skip_count += 1
            continue
        
        # Search for images
        image_urls = search_ddg_images(query, max_results=args.max_results)
        
        # Try to download images
        downloaded = False
        if image_urls:
            for idx, url in enumerate(image_urls):
                print(f"  Trying image {idx + 1}/{len(image_urls)}...")
                if download_and_resize_image(url, output_file, max_size=max_size, quality=args.quality):
                    print(f"  ✓ Saved: {output_file.name}")
                    downloaded = True
                    success_count += 1
                    break
        
        if not downloaded:
            print(f"  ✗ Failed to download image for '{filename}'")
            fail_count += 1
        
        # Delay to avoid rate limiting (except for last item)
        if i < len(items):
            time.sleep(args.delay)
        
        print()
    
    # Print summary
    print("=" * 70)
    print("✓ Download complete!")
    print(f"  Output directory: {output_dir}")
    print(f"\nStatistics:")
    print(f"  ✓ Downloaded:  {success_count}")
    print(f"  ⊙ Skipped:     {skip_count}")
    print(f"  ✗ Failed:      {fail_count}")
    print(f"  Total:         {len(items)}")
    print("=" * 70)


if __name__ == "__main__":
    main()

