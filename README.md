# TikTok Mass Archiver
A set of scripts and related repos to mass-save public TikTok content. Has support for saving both **videos** and **photo sets** from individual posts, user accounts or collections.

NOTE: This repo is meant to work on Windows but should be trivial to change it for MacOS/Linux. Just change the batch files in `scripts/` and the subprocess commands in `save_media.py` accordingly.

## Requirements
- Python 3.11 (minimum)
- Git client

## Setup
```bash
git clone --recurse-submodules https://github.com/tejashah88/tiktok-mass-archiver.git
cd tiktok-mass-archiver

# Install dependencies for yt-dlp and TikTok-Multi-Downloader
call scripts/setup.cmd

# Test that dependencies for yt-dlp and TikTok-Multi-Downloader were installed
call scripts/test.cmd
```

## Usage
NOTE: The following links are templates. Any links you provide should match this template.
```bash
# Download the video from a post
python save_media.py https://www.tiktok.com/@username123/video/0123456789123456789

# Download the photo set from a post
python save_media.py https://www.tiktok.com/@username123/photo/0123456789123456789

# Download all posts from a user
python save_media.py https://www.tiktok.com/@username123

# Download all posts from a collection
python save_media.py https://www.tiktok.com/@username123/collection/COLLECTION-0123456789123456789
python save_media.py https://www.tiktok.com/t/XXXXXXXX/
```

NOTE: Make sure to check for any posts that weren't fetched in `TikTok-Multi-Downloader\errors.txt`

## Development

### Updating from master
```bash
# Pull latest changes from main repo
git pull origin master

# Update submodules by pulling for each one
git submodule update --recursive --remote
```
