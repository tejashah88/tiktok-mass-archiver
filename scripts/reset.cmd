@REM Call this in case the setup failed and we need to roll-back
call deactivate.bat

rmdir /S /Q .\yt-dlp\env
rmdir /S /Q .\TikTok-Multi-Downloader\env
