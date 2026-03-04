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
    
    photo_extensions = ['.jpg', '.jpeg', '.png', '.gif']
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
    
    # Get media from the site subdirectory
    site_path = f"{climb_path}/site"
    photos, videos = list_media(site_path)
    
    print(f"  Found {len(photos)} photo(s) and {len(videos)} video(s) in site directory")
    
    if not photos and not videos:
        print(f"  Skipping {climb_name} - no media in 'site' directory")
        continue
    
    # Create filename-safe slug
    slug = re.sub(r'[^a-z0-9]+', '-', climb_name.lower()).strip('-')
    
    # Create shared links for all photos
    photo_urls = []
    for photo in photos:
        photo_name = photo['name']
        dropbox_path = photo['path_lower']
        
        print(f"  Creating shared link for photo: {photo_name}...")
        shared_url = create_shared_link(dropbox_path)
        
        if shared_url:
            photo_urls.append(shared_url)
        else:
            print(f"  Warning: Skipping {photo_name} (no shared link created)")
    
    # Create shared links for all videos
    video_urls = []
    for video in videos:
        video_name = video['name']
        dropbox_path = video['path_lower']
        
        print(f"  Creating shared link for video: {video_name}...")
        shared_url = create_shared_link(dropbox_path)
        
        if shared_url:
            video_urls.append(shared_url)
        else:
            print(f"  Warning: Skipping {video_name} (no shared link created)")
    
    if not photo_urls and not video_urls:
        print(f"  Skipping {climb_name} - no media could be shared")
        continue
    
    # Create markdown file in _climbing
    filename = f"_climbing/{slug}.md"
    
    with open(filename, 'w') as f:
        f.write("---\n")
        f.write("layout: climbing\n")
        f.write(f'title: "{climb_name}"\n')
        f.write(f"date: {date.today()}\n")
        f.write(f"permalink: /climbing/{slug}.html\n")
        
        if photo_urls:
            f.write("photos:\n")
            for url in photo_urls:
                f.write(f"  - {url}\n")
        
        if video_urls:
            f.write("videos:\n")
            for url in video_urls:
                f.write(f"  - {url}\n")
        
        f.write("---\n")
        f.write("\n")
        f.write(f"Photos from {climb_name}.\n")
    
    print(f"  Created: {filename}")
    print(f"  Generated {len(photo_urls)} photo link(s) and {len(video_urls)} video link(s)")

print(f"\nDone! Generated climbing pages with shared Dropbox links")
