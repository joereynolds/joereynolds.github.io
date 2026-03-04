#!/usr/bin/env python3
import os
import json
import requests
from datetime import date
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
    
    # Create shared links for thumbnails and compressed images
    thumbnail_urls = []
    compressed_urls = []
    
    for thumb, comp in matched_pairs:
        thumb_name = thumb['name']
        comp_name = comp['name']
        
        print(f"  Creating shared links for: {thumb_name} / {comp_name}...")
        
        thumb_url = create_shared_link(thumb['path_lower'])
        comp_url = create_shared_link(comp['path_lower'])
        
        if thumb_url and comp_url:
            thumbnail_urls.append(thumb_url)
            compressed_urls.append(comp_url)
        else:
            print(f"  Warning: Skipping pair (could not create shared links)")
    
    if not thumbnail_urls or not compressed_urls:
        print(f"  Skipping {climb_name} - no image pairs could be shared")
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
        for url in thumbnail_urls:
            f.write(f"  - {url}\n")
        
        f.write("compressed:\n")
        for url in compressed_urls:
            f.write(f"  - {url}\n")
        
        f.write("---\n")
        f.write("\n")
        f.write(f"Photos from {climb_name}.\n")
    
    print(f"  Created: {filename}")
    print(f"  Generated {len(thumbnail_urls)} thumbnail/compressed pair(s)")

print(f"\nDone! Generated climbing pages with shared Dropbox links")
