@REM Delete the existing environments in case any dependencies for yt-dlp and TikTok-Multi-Downloader have changed
call scripts/reset.cmd

@REM Install updated dependencies for yt-dlp and TikTok-Multi-Downloader
call scripts/setup.cmd
