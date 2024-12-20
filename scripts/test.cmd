@REM Test yt-dlp application
cd yt-dlp

call env/Scripts/activate.bat
call yt-dlp.cmd --help
call deactivate.bat
cd ..

@REM Test TikTok-Multi-Downloader program
cd TikTok-Multi-Downloader

call env/Scripts/activate.bat
python multitok.py --help

call deactivate.bat
cd ..
