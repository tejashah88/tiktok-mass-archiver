@REM Pull latest changes from main repo
git pull origin main

@REM Update submodules by pulling for each one
git submodule update --recursive --remote
