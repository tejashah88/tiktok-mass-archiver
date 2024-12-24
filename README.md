# TikTok Mass Archiver
A set of scripts and related repos to mass-save **public** TikTok content. Supports saving both **videos** and **photo sets** from individual posts, user accounts or collections, with incremental updating.

NOTE: This repo is meant to work on Windows but should be trivial to change it for MacOS/Linux. Just change the batch files in `scripts/` and the subprocess commands in `save_media.py` accordingly.

NOTE: Downloading of private liked and favorited posts is **NOT** supported! See [the note below](#note-about-downloading-private-data-for-developers) about what needs to be done.

## Table of Contents
  * [Requirements](#requirements)
  * [Setup](#setup)
  * [Usage](#usage)
    * [Usage Help](#usage-help)
    * [Creating and using a "download" script](#creating-and-using-a-download-script)
    * [Error checking](#error-checking)
  * [Development](#development)
    * [Updating from main branch](#updating-from-main-branch)
    * [Note about downloading private data (for developers)](#note-about-downloading-private-data-for-developers)

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

# Download all posts from a collection to a different output directory...
## Relative to project root directory
python save_media.py https://www.tiktok.com/t/XXXXXXXX/ --output-dir path/to/archive
## Via an absolute directory path
python save_media.py https://www.tiktok.com/t/XXXXXXXX/ --output-dir "C:\Users\Bob The Builder\Archive"
```

### Usage Help
```bash
usage: save_media.py [-h] [--output-dir DIR] [--only-links] [--only-media] url

Save public TikTok data for archiving purposes.

positional arguments:
  url               TikTok post/user/collection URL

options:
  -h, --help        show this help message and exit
  --output-dir DIR  Specify the output directory for all saved media. Defaults to <PROJECT_ROOT>/saved-data
  --only-links      Only download the collection or user post links. Does nothing for individual posts.
  --only-media      Only download media from existing links if it exists. Does nothing for individual posts.
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

### Note about downloading private data (for developers)
This project does not directly support downloading your liked or favorited posts from your personal account, but you can at least grab those lists with `jq` and an export of your TikTok data.

```bash
type user_data_tiktok.json | jq -r ".Activity.\"Like List\".ItemFavoriteList[].link" > personal_likes.txt
type user_data_tiktok.json | jq -r ".Activity.\"Favorite Videos\".FavoriteVideoList[].Link" > personal_favorites.txt
```

The links will be in the format of "https://www.tiktokv.com/share/video/0123456789123456789/", which isn't ideal since we don't have username information that's needed for `TikTok-Multi-Downloader`. Additionally, trying to do 301 resolves doesn't work as expected since it resolves to "https://www.tiktok.com/@/video/0123456789123456789/", and then changes the URL via some suspected JavaScript. You can still get the original video otherwise, and if you're willing to tinker with the downloader code, it'll work with minimal fuss.
