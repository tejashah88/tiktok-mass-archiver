# TikTok Mass Archiver
A set of scripts and related repos to mass-save public TikTok content. Supports saving both **videos** and **photo sets** from individual posts, user accounts or collections, with incremental updating.

NOTE: This repo is meant to work on Windows but should be trivial to change it for MacOS/Linux. Just change the batch files in `scripts/` and the subprocess commands in `save_media.py` accordingly.

## Requirements
- Python 3.11 (minimum)
- Git client
- jq (Install on windows with `winget install jqlang.jq`)

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

# Download only links from user or collection (saved to saved-data/links)
python save_media.py https://www.tiktok.com/@username123 --only-links
python save_media.py https://www.tiktok.com/t/XXXXXXXX/ --only-links

# Download only media from set of existing links from user or collection (saved to saved-data/media)
python save_media.py https://www.tiktok.com/@username123 --only-media
python save_media.py https://www.tiktok.com/t/XXXXXXXX/ --only-media
```

### Usage Help
```bash
usage: save_media.py [-h] [--only-links] [--only-media] url

Save public TikTok data for archiving

positional arguments:
  url           TikTok post/user/collection URL

options:
  -h, --help    show this help message and exit
  --only-links  Only download the collection or user post links. Does nothing for individual posts.
  --only-media  Only download media from existing links if it exists. Does nothing for individual posts.
```

### Creating and using a "download" script
If you have multiple users or collections that you want to download, either as one giant dump or incrementally, I'd recommend creating a `run.cmd` or similarly named file with all the `python save_media.py <URL>` commands. Here's an example `run.cmd` file:

```bat
@REM Save a bunch of collections
python save_media.py https://www.tiktok.com/t/XXXXXXXX/
python save_media.py https://www.tiktok.com/t/XXXXXXXX/
python save_media.py https://www.tiktok.com/t/XXXXXXXX/

@REM Save a bunch of user posts
python save_media.py https://www.tiktok.com/@username123
python save_media.py https://www.tiktok.com/@username123
python save_media.py https://www.tiktok.com/@username123
```

You can invoke it with `call run.cmd` in Windows command prompt.

### Error checking
Make sure to check for any posts that weren't fetched in `TikTok-Multi-Downloader\errors.txt`. In order to make sure all your desired media is downloaded, you'll have to run the command at least 2 or 3 times.

## Development

### Updating from main branch
```bash
# Pull latest changes from main repo
git pull origin main

# Update submodules by pulling for each one
git submodule update --recursive --remote
```
