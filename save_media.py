import argparse
import os
import sys
from urllib.parse import urlparse

from utils import resolve_redirects, expand_tt_post_links, download_tt_media


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save public TikTok data for archiving purposes.')

    parser.add_argument("url", help="TikTok post/user/collection URL")
    parser.add_argument("--output-dir", metavar="DIR", default="saved-data", help="Specify the output directory for all saved media. Defaults to <PROJECT_ROOT>/saved-data")
    parser.add_argument("--only-links", action="store_true", help="Only download the collection or user post links. Does nothing for individual posts.")
    parser.add_argument("--only-media", action="store_true", help="Only download media from existing links if it exists. Does nothing for individual posts.")

    args = parser.parse_args()
    tt_url = args.url
    output_dir = args.output_dir
    only_links = args.only_links
    only_media = args.only_media

    if not tt_url.startswith('https://www.tiktok.com/'):
        print('The given URL is not a TikTok URL')
        sys.exit(1)

    if only_links and only_media:
        print('"--only-links" and "--only-media" are mutually exclusive. See --help for more information.')
        sys.exit(1)

    # Resolve for final URL in case it's a short link
    tt_resolved_url = resolve_redirects(tt_url)
    if not tt_resolved_url:
        print('The given URL was not resolvable')
        sys.exit(1)

    tt_clean_url = tt_resolved_url.split('?')[0]
    print(f'Resolved clean URL: {tt_clean_url}')

    # Define relevent output directories
    LINKS_DIR = os.path.join(output_dir, 'links')
    MEDIA_DIR = os.path.join(output_dir, 'media')
    COL_MEDIA_DIR   = os.path.join(MEDIA_DIR, 'collection')
    POSTS_MEDIA_DIR = os.path.join(MEDIA_DIR, 'posts')
    USER_MEDIA_DIR  = os.path.join(MEDIA_DIR, 'user')

    # Create output directories if needed
    os.makedirs(LINKS_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)
    os.makedirs(COL_MEDIA_DIR, exist_ok=True)
    os.makedirs(POSTS_MEDIA_DIR, exist_ok=True)
    os.makedirs(USER_MEDIA_DIR, exist_ok=True)

    if '/video/' in tt_resolved_url or '/photo/' in tt_clean_url:
        # The link is an individual post

        resource_raw_slug = str(urlparse(tt_clean_url).path).split('/')[1::2]
        final_slug = '-'.join(resource_raw_slug)[1:]

        # Create or append a temporary text file for the singular link
        SAVED_LINKS_FILE = os.path.join(LINKS_DIR, 'posts.txt')
        with open(SAVED_LINKS_FILE, 'w') as fp:
            fp.write(tt_clean_url)

        # Download all media from scraped links
        download_tt_media(SAVED_LINKS_FILE, POSTS_MEDIA_DIR)
    else:
        # The link has a collection of post links

        # Get string slug for creating output resources
        resource_raw_slug = str(urlparse(tt_clean_url).path).split('/')[-1]
        if '@' in resource_raw_slug:
            resource_type = 'user'
            final_slug = resource_raw_slug[1:]
        else:
            # HACK: Assuming it's a collection link. This is brittle
            resource_type = 'collection'
            final_slug = resource_raw_slug

        SAVED_LINKS_FILE = os.path.join(LINKS_DIR, f'{resource_type}-{final_slug}.txt')
        if not only_media:
            # Gather all post links into a single text file
            expand_tt_post_links(tt_clean_url, SAVED_LINKS_FILE)

        if not only_links:
            # Ensure necessary directories are created
            SAVED_MEDIA_DIR = os.path.join(MEDIA_DIR, resource_type, final_slug)

            # Download all media from scraped links
            download_tt_media(SAVED_LINKS_FILE, SAVED_MEDIA_DIR)
