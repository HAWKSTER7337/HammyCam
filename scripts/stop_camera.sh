#!/bin/bash
# Stop HammyCam

echo "Stopping HammyCam..."

# Stop FFmpeg
if [ -f /tmp/hammycam_ffmpeg.pid ]; then
    FFMPEG_PID=$(cat /tmp/hammycam_ffmpeg.pid)
    if kill -0 $FFMPEG_PID 2>/dev/null; then
        kill $FFMPEG_PID 2>/dev/null
        echo "✓ Stopped FFmpeg (PID: $FFMPEG_PID)"
    fi
    rm /tmp/hammycam_ffmpeg.pid
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
pkill -f "ffmpeg.*current_frame" 2>/dev/null && echo "✓ Cleaned up remaining FFmpeg processes"

# Remove current frame
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
rm -f "$SCRIPT_DIR/../web/current_frame.jpg"
echo "✓ Removed current_frame.jpg"

echo "HammyCam stopped."
