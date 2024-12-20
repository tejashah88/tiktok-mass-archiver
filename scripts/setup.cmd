@REM Setup yt-dlp application
cd yt-dlp

python -m venv env
call env/Scripts/activate.bat

python -m pip install --upgrade pip
pip install hatch
hatch run setup

call deactivate.bat
cd ..

@REM Setup TikTok-Multi-Downloader program
cd TikTok-Multi-Downloader

python -m venv env
call env/Scripts/activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

call  deactivate.bat
cd ..

@REM yt-dlp.cmd --flat-playlist -J https://www.tiktok.com/t/ZTYXgdDGX/ | ..\bin\jq.exe -r ".entries[].url" > links/links_20.txt
