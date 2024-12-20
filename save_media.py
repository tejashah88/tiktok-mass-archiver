import re
import os
import sys
import subprocess
import http.client
from urllib.parse import urlparse, urljoin

def resolve_redirects(url):
    try:
        # Loop to handle multiple redirects until the final URL is resolved
        while True:
            parsed_url = urlparse(url)
            # Choose the appropriate connection type
            if parsed_url.scheme == 'https':
                connection = http.client.HTTPSConnection(parsed_url.netloc)
            elif parsed_url.scheme == 'http':
                connection = http.client.HTTPConnection(parsed_url.netloc)
            else:
                raise ValueError('Unsupported URL scheme: only HTTP and HTTPS are supported')

            path = parsed_url.path or '/'
            if parsed_url.query:
                path += f'?{parsed_url.query}'

            # Send HEAD request to avoid downloading the full content
            connection.request('HEAD', path)
            response = connection.getresponse()

            # Check for redirects (301 or 302)
            if response.status in (301, 302):
                location = response.getheader('Location')
                if not location:
                    raise ValueError('Redirect response missing "Location" header.')
                # Resolve relative redirects
                url = urljoin(url, location)
            else:
                # No more redirects
                return url
    except Exception as e:
        print(f'Error occurred: {e}')
        return None


def expand_tt_post_links(url, links_filename):
    SAVED_LINKS_FILE = os.path.join('saved-data', 'links', links_filename)

    try:
        commands = [
            "cd yt-dlp",
            "call env/Scripts/activate.bat",
            f'call yt-dlp.cmd --flat-playlist -J {url} | ..\\bin\\jq.exe -r ".entries[].url" > ..\\{SAVED_LINKS_FILE}',
            "call deactivate.bat",
            "cd .."
        ]

        # Join the commands using '&&' for sequential execution
        full_command = " && ".join(commands)

        print("Starting yt-dlp to collect TikTok post links...")
        with subprocess.Popen(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as process:
            for line in process.stdout:
                print(line, end='', flush=True)

        if process.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with errors")

    except Exception as e:
        print(f"Error occurred: {e}")


def download_tt_media(links_filename, output_dir):
    SAVED_LINKS_FILE = os.path.join('saved-data', 'links', links_filename)

    try:
        commands = [
            "cd TikTok-Multi-Downloader",
            "call env/Scripts/activate.bat",
            f'python multitok.py --links ..\\{SAVED_LINKS_FILE} --no-watermark --skip-existing --workers 4 --api-version v3 --no-folders --output-dir "..\\{output_dir}"',
            "call deactivate.bat",
            "cd .."
        ]

        # Join the commands using '&&' for sequential execution
        full_command = " && ".join(commands)

        print("Starting Tiktok-Multi-Downloader to fetch TikTok media...")
        with subprocess.Popen(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as process:
            for line in process.stdout:
                print(line, end='', flush=True)

        if process.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with errors")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python save_media.py <URL>')
        sys.exit(1)

    tt_url = sys.argv[1]
    if not tt_url.startswith('https://www.tiktok.com/'):
        print('The given URL is not a TikTok URL')
        sys.exit(1)

    # Resolve for final URL in case it's a short link
    tt_resolved_url = resolve_redirects(tt_url)
    if not tt_resolved_url:
        print('The given URL was not resolvable')
        sys.exit(1)

    print(f'Resolved URL: {tt_resolved_url}')
    if '/video/' in tt_resolved_url or '/photo/' in tt_resolved_url:
        # The link is an individual post

        resource_raw_slug = str(urlparse(tt_resolved_url).path).split('/')[1::2]
        final_slug = '-'.join(resource_raw_slug)[1:]
        print(final_slug)

        # Create or append a temporary text file for the singular link
        SAVED_LINKS_FILE = os.path.join('saved-data', 'links', 'posts.txt')
        with open(SAVED_LINKS_FILE, 'a') as fp:
            fp.write(tt_resolved_url)

        # Ensure necessary directories are created
        SAVED_MEDIA_DIR = os.path.join('saved-data', 'media', 'posts')
        os.makedirs(SAVED_MEDIA_DIR, exist_ok=True)

        # Download all media from scraped links
        download_tt_media('posts.txt', SAVED_MEDIA_DIR)
    else:
        # The link has a collection of post links

        # Get string slug for creating output resources
        resource_raw_slug = str(urlparse(tt_resolved_url).path).split('/')[-1]
        if '@' in resource_raw_slug:
            resource_type = 'user'
            final_slug = resource_raw_slug[1:]
        else:
            # HACK: Assuming it's a collection link. This is brittle
            resource_type = 'collection'
            final_slug = resource_raw_slug

        # Gather all post links into a single text file
        expand_tt_post_links(tt_resolved_url, f'{resource_type}-{final_slug}.txt')

        # Ensure necessary directories are created
        SAVED_MEDIA_DIR = os.path.join('saved-data', 'media', resource_type, final_slug)
        os.makedirs(SAVED_MEDIA_DIR, exist_ok=True)

        # Download all media from scraped links
        download_tt_media(f'{resource_type}-{final_slug}.txt', SAVED_MEDIA_DIR)



