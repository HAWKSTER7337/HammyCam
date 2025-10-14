#!/bin/bash
# Simple web camera using frame updates

IMAGE="${1:-}"
WIDTH="${2:-1280}"
HEIGHT="${3:-720}"
FPS="${4:-30}"
PORT="${5:-8080}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WEB_DIR="$PROJECT_ROOT/web"

echo "=== Simple HammyCam Web Viewer ==="
echo "Port: $PORT"
echo "Resolution: ${WIDTH}x${HEIGHT}"
echo ""

# Start Python web server from web directory
cd "$WEB_DIR"
python3 -m http.server "$PORT" --bind 0.0.0.0 > /tmp/web_server.log 2>&1 &
WEB_PID=$!
echo "$WEB_PID" > /tmp/hammycam_webserver.pid

sleep 2

echo "🌐 Open in browser:"
echo "   http://localhost:${PORT}/simple_web_viewer.html"
echo ""
CONTAINER_IP=$(hostname -I | awk '{print $1}')
if [ -n "$CONTAINER_IP" ]; then
    echo "   http://${CONTAINER_IP}:${PORT}/simple_web_viewer.html"
fi
echo ""

# Generate frames continuously
if [ -n "$IMAGE" ] && [ -f "$IMAGE" ]; then
    echo "Mode: Image ($IMAGE)"
    ffmpeg -re -loop 1 -framerate "$FPS" -i "$IMAGE" \
        -vf "scale=${WIDTH}:${HEIGHT},drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{localtime\:%X}':fontcolor=white:fontsize=24:x=10:y=10:box=1:boxcolor=black@0.5:boxborderw=5" \
        -q:v 3 -y -update 1 "$WEB_DIR/current_frame.jpg"
else
    echo "Mode: Test Pattern"
    ffmpeg -f lavfi -i "color=c=blue:s=${WIDTH}x${HEIGHT}:r=${FPS}" \
        -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='HammyCam':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-40:box=1:boxcolor=black@0.5:boxborderw=5,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{localtime\:%X}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2+40:box=1:boxcolor=black@0.5:boxborderw=5" \
        -q:v 3 -y -update 1 "$WEB_DIR/current_frame.jpg"
fi

# Cleanup
if [ -f /tmp/hammycam_webserver.pid ]; then
    kill $(cat /tmp/hammycam_webserver.pid) 2>/dev/null
    rm /tmp/hammycam_webserver.pid
fi

