#!/bin/bash
# Stop HammyCam

echo "Stopping HammyCam..."

# Stop web camera
if [ -f /tmp/hammycam_web.pid ]; then
    WEB_PID=$(cat /tmp/hammycam_web.pid)
    if kill -0 $WEB_PID 2>/dev/null; then
        kill $WEB_PID 2>/dev/null
        echo "✓ Stopped web camera (PID: $WEB_PID)"
    fi
    rm /tmp/hammycam_web.pid
fi

# Stop web server
if [ -f /tmp/hammycam_webserver.pid ]; then
    WEBSERVER_PID=$(cat /tmp/hammycam_webserver.pid)
    if kill -0 $WEBSERVER_PID 2>/dev/null; then
        kill $WEBSERVER_PID 2>/dev/null
        echo "✓ Stopped web server (PID: $WEBSERVER_PID)"
    fi
    rm /tmp/hammycam_webserver.pid
fi

# Cleanup any remaining processes
pkill -f "simple_web_camera" 2>/dev/null && echo "✓ Cleaned up remaining processes"

# Remove current frame
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
rm -f "$SCRIPT_DIR/../web/current_frame.jpg"

echo "HammyCam stopped."

