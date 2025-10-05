import argparse
import os
import sys

from utils import download_tt_media


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download TikTok posts from list of links for archiving purposes.')

    parser.add_argument("path", help="Path to list of links (txt)")
    parser.add_argument("--output-dir", metavar="DIR", default="saved-data", help="Specify the output directory for all saved media. Defaults to <PROJECT_ROOT>/saved-data")

    args = parser.parse_args()
    path_to_links = args.path
    output_dir = args.output_dir

    # Check if a valid TXT file is specified
    path_exists = os.path.exists(path_to_links)
    path_is_file = os.path.isfile(path_to_links)
    path_is_txt_file = os.path.splitext(path_to_links[1]) != '.txt'
    if not path_exists or not path_is_file or not path_is_txt_file:
        print('The given path either does not exist, is a directory or does not have a .txt extension')
        sys.exit(1)

    # Define relevent output directories
    MEDIA_DIR = os.path.join(output_dir, 'media')
    POSTS_MEDIA_DIR = os.path.join(MEDIA_DIR, 'posts')

    # Create output directories if needed
    os.makedirs(POSTS_MEDIA_DIR, exist_ok=True)

    # Download all media from scraped links
    download_tt_media(path_to_links, POSTS_MEDIA_DIR)
