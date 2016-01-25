# Activate Headless Display (Xvfb)

sudo Xvfb -ac :99 -screen 0 1280x1024x16 > /dev/null 2>&1 &
export DISPLAY=:99
exec "$@"
