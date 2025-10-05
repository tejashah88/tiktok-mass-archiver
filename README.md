# TikTok Mass Archiver
A commandline program to mass-save public TikTok content. Supports saving both videos and photo sets from individual posts, user accounts or public collections, with incremental updating and resilient retry logic.

NOTE: This repo is meant to work on Windows but should be trivial to change it for MacOS/Linux. Just change the batch files in `scripts/` and the subprocess commands in `save_media.py` accordingly.

NOTE: Downloading of private liked and favorited posts is **NOT fully** supported! See [the note below](#note-about-downloading-liked-and-favorited-videos) about what needs to be done.

## Table of Contents
  * [Features](#features)
  * [Requirements](#requirements)
  * [Setup](#setup)
  * [Applying New Updates](#applying-new-updates)
  * [Usage](#usage)
    * [Usage Help](#usage-help)
    * [Creating and using a download script](#creating-and-using-a-download-script)
    * [Error checking](#error-checking)
  * [Development](#development)
    * [Updating from main branch](#updating-from-main-branch)
    * [Note about downloading liked and favorited videos](#note-about-downloading-liked-and-favorited-videos)


## Features
- [X] Download individual posts (video and photo set both supported)
- [X] Download all posts from a user or public collection
- [X] All media is downloaded without watermarking
- [X] Save to any output directory of choice, ideal for use with external drives
- [X] Resilient to slow/unstable internet connection with generous retry logic
- [X] Run speedy incremental updates on user posts or collections
- [X] Use in batch script for automatically archiving against multiple sources

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

## Applying New Updates
This project will be updated as needed to fix bugs and add new features. It's highly recommended to do this often, especially in the wake of the turbulence of TikTok politics (as of early 2025).

```bash
# Pull from the main branch of this repository (as hosted on github.com)
call scripts/update.cmd

# Reset and reinstall the environments for yt-dlp and TikTok-Multi-Downloader
call scripts/reinstall.cmd
```

**NOTE**: If you downloaded this project prior to 1/23/2025, you'll need to explicitly run the `git` update commands, but afterwards the `call scripts/update.cmd` will work as intended.

```bash
# Pull latest changes from main repo
git pull origin main

# Update submodules by pulling for each one
git submodule update --recursive --remote

# Reset and reinstall the environments for yt-dlp and TikTok-Multi-Downloader
call scripts/reinstall.cmd
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

# Download all posts from a collection to a different output directory (make sure to add double-quotes)
## Relative to project root directory
python save_media.py https://www.tiktok.com/t/XXXXXXXX/ --output-dir "path/to/archive"
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

### Creating and using a download script
If you have multiple users or collections that you want to download, either as one giant dump or incrementally, I'd recommend creating a `run.cmd` or similarly named file with all the `python save_media.py <URL>` commands. Here's an example `run.cmd` file:

```bat
@REM Save a bunch of collections
python save_media.py https://www.tiktok.com/t/XXXXXXXX/
python save_media.py https://www.tiktok.com/t/YYYYYYYY/
python save_media.py https://www.tiktok.com/t/ZZZZZZZZ/

@REM Save a bunch of user posts
python save_media.py https://www.tiktok.com/@username123 --output-dir path/to/media
python save_media.py https://www.tiktok.com/@username456 --output-dir path/to/media
python save_media.py https://www.tiktok.com/@username789 --output-dir path/to/media
```

You can invoke it with `call run.cmd` in Windows command prompt.

### Error checking
Make sure to check for any posts that weren't fetched in `TikTok-Multi-Downloader\errors.txt`. In order to make sure all your desired media is downloaded, you'll have to run the command at least 2 or 3 times.

## Development

### Updating from main branch
```bash
# Pull from the main branch of this repository (as hosted on github.com)
call scripts/update.cmd

# Reset and reinstall the environments for yt-dlp and TikTok-Multi-Downloader
call scripts/reinstall.cmd
```

### Note about downloading liked and favorited videos
This project does not directly support downloading your liked or favorited posts from your personal account, but you can at least grab those lists with `jq` and an export of your TikTok data.

```bash
type user_data_tiktok.json | jq -r ".Activity.\"Like List\".ItemFavoriteList[].link" > personal_likes.txt
type user_data_tiktok.json | jq -r ".Activity.\"Favorite Videos\".FavoriteVideoList[].Link" > personal_favorites.txt
```

After extracting the links, you can extract your videos/photosets from that file path with the following syntax:
```bash
python extract_from_file.py personal_likes.txt     --output-dir "path/to/liked_videos"
python extract_from_file.py personal_favorites.txt --output-dir "path/to/favorited_videos"
```

Note that due to some dynamic javascript shenanigans, these posts will not be categorized per-creator. Additionally, it's recommended to run this script a few times since some "removed posts" can be the result of making too many requests to TikTok.

On a technical level, the data exports will have their links in the format of "https://www.tiktokv.com/share/video/0123456789123456789/", which eventually 301-resolve to a URL like "https://www.tiktok.com/@/video/0123456789123456789/". Since the username isn't resolved after redirects and seems to be changed within dyanmic javascript shenanigans, the user handle will be substituted with `@[tiktok-user]` to allow `TikTok-Multi-Downloader` to work.
