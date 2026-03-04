#!/usr/bin/env python3
import os
import json
import requests
from datetime import date
from pathlib import Path
import re

DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')

# If not in environment, try reading from .dropbox_token file
if not DROPBOX_ACCESS_TOKEN and os.path.exists('.dropbox_token'):
    with open('.dropbox_token', 'r') as f:
        DROPBOX_ACCESS_TOKEN = f.read().strip()

print("Starting script...")
print(f"Token present: {bool(DROPBOX_ACCESS_TOKEN)}")

if not DROPBOX_ACCESS_TOKEN:
    print("Error: DROPBOX_ACCESS_TOKEN environment variable not set")
    print("Run: export DROPBOX_ACCESS_TOKEN='your_token'")
    print("Or create a .dropbox_token file with your token")
    exit(1)

# Image storage directory
IMAGES_DIR = Path('images/climbing')
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def dropbox_api_request(endpoint, data=None, exit_on_error=True):
    url = f"https://api.dropboxapi.com/2/{endpoint}"
    headers = {
        'Authorization': f'Bearer {DROPBOX_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=data or {}, timeout=10)
        
        if response.status_code != 200:
            error_msg = f"Error: API {endpoint} returned status {response.status_code}"
            print(error_msg)
            print(f"Response: {response.text}")
            if exit_on_error:
                exit(1)
            else:
                raise Exception(error_msg)
        
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Error: Request to {endpoint} timed out")
        if exit_on_error:
            exit(1)
        else:
            raise

def download_file(dropbox_path, local_path):
    """Download a file from Dropbox to local filesystem"""
    url = "https://content.dropboxapi.com/2/files/download"
    headers = {
        'Authorization': f'Bearer {DROPBOX_ACCESS_TOKEN}',
        'Dropbox-API-Arg': json.dumps({'path': dropbox_path})
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"  Warning: Could not download {dropbox_path}: {response.status_code}")
            return False
        
        # Write file to disk
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"  Warning: Error downloading {dropbox_path}: {e}")
        return False

def create_shared_link(path):
    """Create or get a permanent shared link for a file"""
    # First, try to list existing shared links
    try:
        result = dropbox_api_request('sharing/list_shared_links', {
            'path': path,
            'direct_only': True
        }, exit_on_error=False)
        
        if result.get('links'):
            # Use existing shared link
            url = result['links'][0]['url']
            # Convert to direct download URL
            return url.replace('?dl=0', '?raw=1').replace('&dl=0', '&raw=1')
    except Exception as e:
        print(f"  Note: Could not list existing links: {e}")
    
    # Create new permanent shared link
    try:
        result = dropbox_api_request('sharing/create_shared_link_with_settings', {
            'path': path,
            'settings': {
                'requested_visibility': 'public'
            }
        }, exit_on_error=False)
        url = result['url']
        # Convert to direct download URL
        return url.replace('?dl=0', '?raw=1').replace('&dl=0', '&raw=1')
    except Exception as e:
        print(f"  Warning: Could not create shared link for {path}: {e}")
        return None

def has_site_directory(climb_path):
    """Check if a climbing folder has a 'site' subdirectory"""
    try:
        result = dropbox_api_request('files/list_folder', {'path': climb_path})
        entries = result.get('entries', [])
        
        for entry in entries:
            if entry['.tag'] == 'folder' and entry['name'].lower() == 'site':
                return True
        
        return False
    except Exception as e:
        print(f"  Note: Could not check for site directory in {climb_path}: {str(e)[:100]}")
        return False

def list_folders(path):
    result = dropbox_api_request('files/list_folder', {'path': path})
    folders = [entry['name'] for entry in result.get('entries', []) if entry['.tag'] == 'folder']
    return folders

def list_media(path):
    """List both photos and videos from a folder"""
    result = dropbox_api_request('files/list_folder', {'path': path})
    
    photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v']
    
    photos = []
    videos = []
    
    for entry in result.get('entries', []):
        if entry['.tag'] != 'file':
            continue
        
        name_lower = entry['name'].lower()
        if any(name_lower.endswith(ext) for ext in photo_extensions):
            photos.append(entry)
        elif any(name_lower.endswith(ext) for ext in video_extensions):
            videos.append(entry)
    
    return photos, videos

# Main script
print("Fetching climbing folders from Dropbox...")

climbing_folders = list_folders('/Pictures/Climbing')

print(f"Found {len(climbing_folders)} climb(s)")

for climb_name in climbing_folders:
    print(f"\nProcessing: {climb_name}")
    
    climb_path = f"/Pictures/Climbing/{climb_name}"
    
    # Check if folder has 'site' subdirectory
    print(f"  Checking for 'site' directory...")
    if not has_site_directory(climb_path):
        print(f"  Skipping {climb_name} - no 'site' directory found")
        continue
    
    print(f"  ✓ Has 'site' directory")
    
    # Get media from the site/thumbs and site/compressed subdirectories
    site_path = f"{climb_path}/site"
    thumbs_path = f"{site_path}/thumbs"
    compressed_path = f"{site_path}/compressed"
    
    # Get thumbnails and compressed images
    try:
        thumbnails, _ = list_media(thumbs_path)
        compressed_images, _ = list_media(compressed_path)
    except:
        print(f"  Skipping {climb_name} - missing thumbs/ or compressed/ directories")
        continue
    
    print(f"  Found {len(thumbnails)} thumbnail(s) and {len(compressed_images)} compressed image(s)")
    
    if not thumbnails or not compressed_images:
        print(f"  Skipping {climb_name} - need both thumbs and compressed directories")
        continue
    
    # Match thumbnails with compressed images by filename
    # Thumbnails: filename_thumb.webp, Compressed: filename_compressed.webp
    matched_pairs = []
    
    for thumb in thumbnails:
        thumb_name = thumb['name']
        # Extract base name (remove _thumb.webp)
        if '_thumb.webp' in thumb_name:
            base_name = thumb_name.replace('_thumb.webp', '_compressed.webp')
            
            # Find matching compressed image
            for comp in compressed_images:
                if comp['name'] == base_name:
                    matched_pairs.append((thumb, comp))
                    break
    
    print(f"  Matched {len(matched_pairs)} thumbnail/compressed pair(s)")
    
    if not matched_pairs:
        print(f"  Skipping {climb_name} - no matching thumbnail/compressed pairs found")
        continue
    
    # Create filename-safe slug
    slug = re.sub(r'[^a-z0-9]+', '-', climb_name.lower()).strip('-')
    
    # Create climb-specific directory
    climb_dir = IMAGES_DIR / slug
    climb_dir.mkdir(exist_ok=True)
    thumbs_dir = climb_dir / 'thumbs'
    compressed_dir = climb_dir / 'compressed'
    thumbs_dir.mkdir(exist_ok=True)
    compressed_dir.mkdir(exist_ok=True)
    
    # Download thumbnails and compressed images
    thumbnail_paths = []
    compressed_paths = []
    
    for thumb, comp in matched_pairs:
        thumb_name = thumb['name']
        comp_name = comp['name']
        
        print(f"  Downloading: {thumb_name} / {comp_name}...")
        
        # Download thumbnail
        thumb_local_path = thumbs_dir / thumb_name
        if download_file(thumb['path_lower'], thumb_local_path):
            # Store relative path for use in markdown
            thumbnail_paths.append(f"/images/climbing/{slug}/thumbs/{thumb_name}")
        else:
            print(f"  Warning: Skipping pair (could not download thumbnail)")
            continue
        
        # Download compressed image
        comp_local_path = compressed_dir / comp_name
        if download_file(comp['path_lower'], comp_local_path):
            compressed_paths.append(f"/images/climbing/{slug}/compressed/{comp_name}")
        else:
            print(f"  Warning: Skipping pair (could not download compressed image)")
            continue
    
    if not thumbnail_paths or not compressed_paths:
        print(f"  Skipping {climb_name} - no image pairs could be downloaded")
        continue
    
    # Create markdown file in _climbing
    filename = f"_climbing/{slug}.md"
    
    with open(filename, 'w') as f:
        f.write("---\n")
        f.write("layout: climbing\n")
        f.write(f'title: "{climb_name}"\n')
        f.write(f"date: {date.today()}\n")
        f.write(f"permalink: /climbing/{slug}.html\n")
        
        f.write("thumbnails:\n")
        for path in thumbnail_paths:
            f.write(f"  - {path}\n")
        
        f.write("compressed:\n")
        for path in compressed_paths:
            f.write(f"  - {path}\n")
        
        f.write("---\n")
        f.write("\n")
        f.write(f"Photos from {climb_name}.\n")
    
    print(f"  Created: {filename}")
    print(f"  Downloaded {len(thumbnail_paths)} thumbnail/compressed pair(s)")

print(f"\nDone! Generated climbing pages with local images")
