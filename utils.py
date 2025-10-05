import os
import subprocess
import http.client
from urllib.parse import urlparse, urljoin

# Source: ChatGPT (12/20/2024)
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


def expand_tt_post_links(url, links_path):
    abs_links_path = os.path.abspath(links_path)

    try:
        commands = [
            "cd yt-dlp",
            "call env/Scripts/activate.bat",
            f'call yt-dlp.cmd --flat-playlist -J {url} | jq -r ".entries[].url" > "{abs_links_path}"',
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
            for line in process.stdout: # type: ignore
                print(line, end='', flush=True)

        if process.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with errors")

    except Exception as e:
        print(f"Error occurred: {e}")


def download_tt_media(links_path, output_dir):
    abs_links_path = os.path.abspath(links_path)
    abs_output_dir = os.path.abspath(output_dir)

    try:
        commands = [
            "cd TikTok-Multi-Downloader",
            "call env/Scripts/activate.bat",
            f'python multitok.py --links "{abs_links_path}" --no-watermark --skip-existing --workers 4 --api-version v3 --no-folders --output-dir "{abs_output_dir}"',
            "call deactivate.bat",
            "cd .."
        ]

        # Join the commands using '&&' for sequential execution
        full_command = " && ".join(commands)

        print("Starting TikTok-Multi-Downloader to fetch TikTok media...")
        with subprocess.Popen(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as process:
            for line in process.stdout: # type: ignore
                print(line, end='', flush=True)

        if process.returncode == 0:
            print("Command executed successfully")
        else:
            print("Command failed with errors")

    except Exception as e:
        print(f"Error occurred: {e}")
