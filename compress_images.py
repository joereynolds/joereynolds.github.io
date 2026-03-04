#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from PIL import Image

# Configuration
THUMBNAIL_SIZE = (156, 156)
COMPRESSION_QUALITY = 40  # WebP quality (1-100, higher is better)
MAX_COMPRESSED_WIDTH = 1920  # Max width for compressed images

def create_thumbnail(image_path, output_dir):
    """Create a 156x156 thumbnail of an image (center crop)"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (handles RGBA, etc.)
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Calculate crop box for center crop
            width, height = img.size
            target_width, target_height = THUMBNAIL_SIZE
            
            # Calculate aspect ratios
            img_aspect = width / height
            thumb_aspect = target_width / target_height
            
            # Determine crop dimensions
            if img_aspect > thumb_aspect:
                # Image is wider, crop width
                new_width = int(height * thumb_aspect)
                left = (width - new_width) // 2
                crop_box = (left, 0, left + new_width, height)
            else:
                # Image is taller, crop height
                new_height = int(width / thumb_aspect)
                top = (height - new_height) // 2
                crop_box = (0, top, width, top + new_height)
            
            # Crop to center and resize to exact thumbnail size
            img_cropped = img.crop(crop_box)
            img_resized = img_cropped.resize(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # Save thumbnail as WebP
            filename = Path(image_path).stem + '_thumb.webp'
            output_path = os.path.join(output_dir, filename)
            img_resized.save(output_path, 'WEBP', quality=90, method=6)
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
            
            # Save compressed version as WebP
            filename = Path(image_path).stem + '_compressed.webp'
            output_path = os.path.join(output_dir, filename)
            img.save(output_path, 'WEBP', quality=COMPRESSION_QUALITY, method=6)
            
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
