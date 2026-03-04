#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from PIL import Image

# Configuration
THUMBNAIL_SIZE = (156, 156)
COMPRESSION_QUALITY = 85  # JPEG quality (1-100, higher is better)
MAX_COMPRESSED_WIDTH = 1920  # Max width for compressed images

def create_thumbnail(image_path, output_dir):
    """Create a 156x156 thumbnail of an image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (handles RGBA, etc.)
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Create thumbnail (preserves aspect ratio and fits within box)
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # Create a square canvas and paste the thumbnail centered
            thumb = Image.new('RGB', THUMBNAIL_SIZE, (255, 255, 255))
            offset = ((THUMBNAIL_SIZE[0] - img.size[0]) // 2, 
                      (THUMBNAIL_SIZE[1] - img.size[1]) // 2)
            thumb.paste(img, offset)
            
            # Save thumbnail
            filename = Path(image_path).stem + '_thumb.jpg'
            output_path = os.path.join(output_dir, filename)
            thumb.save(output_path, 'JPEG', quality=90, optimize=True)
            print(f"  Created thumbnail: {filename}")
            return True
    except Exception as e:
        print(f"  Error creating thumbnail for {image_path}: {e}")
        return False

def compress_image(image_path, output_dir):
    """Create a compressed version of an image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Resize if image is too large
            if img.size[0] > MAX_COMPRESSED_WIDTH:
                ratio = MAX_COMPRESSED_WIDTH / img.size[0]
                new_height = int(img.size[1] * ratio)
                img = img.resize((MAX_COMPRESSED_WIDTH, new_height), Image.Resampling.LANCZOS)
            
            # Save compressed version
            filename = Path(image_path).stem + '_compressed.jpg'
            output_path = os.path.join(output_dir, filename)
            img.save(output_path, 'JPEG', quality=COMPRESSION_QUALITY, optimize=True)
            
            # Show compression stats
            original_size = os.path.getsize(image_path) / 1024  # KB
            compressed_size = os.path.getsize(output_path) / 1024  # KB
            savings = ((original_size - compressed_size) / original_size) * 100
            print(f"  Compressed: {filename} ({original_size:.1f}KB → {compressed_size:.1f}KB, saved {savings:.1f}%)")
            return True
    except Exception as e:
        print(f"  Error compressing {image_path}: {e}")
        return False

def process_directory(directory):
    """Process all images in a directory"""
    directory = Path(directory).resolve()
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory")
        return
    
    # Create output directories
    thumbs_dir = directory / 'thumbs'
    compressed_dir = directory / 'compressed'
    thumbs_dir.mkdir(exist_ok=True)
    compressed_dir.mkdir(exist_ok=True)
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    # Find all images
    images = [f for f in directory.iterdir() 
              if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not images:
        print(f"No images found in {directory}")
        return
    
    print(f"Found {len(images)} image(s) in {directory}")
    print(f"Creating thumbnails ({THUMBNAIL_SIZE[0]}x{THUMBNAIL_SIZE[1]}) and compressed versions...")
    print()
    
    thumb_count = 0
    compress_count = 0
    
    for image_path in sorted(images):
        print(f"Processing: {image_path.name}")
        
        if create_thumbnail(image_path, thumbs_dir):
            thumb_count += 1
        
        if compress_image(image_path, compressed_dir):
            compress_count += 1
        
        print()
    
    print(f"Done!")
    print(f"  Thumbnails created: {thumb_count} (in {thumbs_dir})")
    print(f"  Compressed images: {compress_count} (in {compressed_dir})")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 compress_images.py <directory>")
        print("Example: python3 compress_images.py /path/to/images")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_directory(directory)
