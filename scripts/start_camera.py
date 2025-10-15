#!/usr/bin/env python3
"""
Auto-start script for HammyCam
Reads configuration and starts the appropriate camera
"""

import yaml
import subprocess
import sys
import os
import time
from pathlib import Path


def load_config():
    """Load camera configuration from YAML file"""
    config_path = Path(__file__).parent.parent / "camera_config.yaml"

    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def start_web_camera(config):
    """Start the web camera with FFmpeg directly"""
    camera = config["camera"]
    display_config = config.get("display", {})

    mode = camera["mode"]
    width = camera["width"]
    height = camera["height"]
    fps = camera["fps"]
    web_port = display_config.get("web_port", 8080)

    project_root = Path(__file__).parent.parent
    web_dir = project_root / "web"
    output_file = web_dir / "current_frame.jpg"

    print("=" * 60)
    print("  HammyCam Web Camera")
    print("=" * 60)
    print(f"Mode: {mode}")
    print(f"Resolution: {width}x{height} @ {fps}fps")
    print(f"Web Port: {web_port}")
    print(f"Output: {output_file}")
    print("=" * 60)

    # Start Python HTTP server
    print("\n📡 Starting web server...")
    webserver_log = open("/tmp/hammycam_webserver.log", "w")
    webserver_process = subprocess.Popen(
        ["python3", "-m", "http.server", str(web_port), "--bind", "0.0.0.0"],
        stdout=webserver_log,
        stderr=subprocess.STDOUT,
        cwd=str(web_dir),
    )

    # Save web server PID
    Path("/tmp/hammycam_webserver.pid").write_text(str(webserver_process.pid))
    print(f"✓ Web server started (PID: {webserver_process.pid})")

    # Wait for server to start
    time.sleep(1)

    # Build FFmpeg command
    print("\n📹 Starting FFmpeg camera...")

    if mode == "image":
        # Image mode
        image_path = project_root / camera.get("image_path", "images/black.jpg")

        ffmpeg_cmd = [
            "ffmpeg",
            "-re",  # Read at native frame rate
            "-loop",
            "1",  # Loop the image
            "-framerate",
            str(fps),
            "-i",
            str(image_path),
            "-vf",
            (
                f"scale={width}:{height},"
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                "text='HammyCam %{localtime\\:%X}':"
                "fontcolor=white:fontsize=24:x=10:y=10:"
                "box=1:boxcolor=black@0.5:boxborderw=5"
            ),
            "-q:v",
            "3",  # Quality
            "-y",  # Overwrite
            "-update",
            "1",  # Update same file
            str(output_file),
        ]
    else:
        # Test pattern mode
        ffmpeg_cmd = [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            f"color=c=blue:s={width}x{height}:r={fps}",
            "-vf",
            (
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                "text='HammyCam':"
                "fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2-40:"
                "box=1:boxcolor=black@0.5:boxborderw=5,"
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                "text='%{localtime\\:%X}':"
                "fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2+40:"
                "box=1:boxcolor=black@0.5:boxborderw=5"
            ),
            "-q:v",
            "3",
            "-y",
            "-update",
            "1",
            str(output_file),
        ]

    # Start FFmpeg
    ffmpeg_log = open("/tmp/hammycam_ffmpeg.log", "w")
    ffmpeg_process = subprocess.Popen(
        ffmpeg_cmd, stdout=ffmpeg_log, stderr=subprocess.STDOUT
    )

    # Save FFmpeg PID
    Path("/tmp/hammycam_ffmpeg.pid").write_text(str(ffmpeg_process.pid))
    print(f"✓ FFmpeg started (PID: {ffmpeg_process.pid})")
    print(f"  Logs: /tmp/hammycam_ffmpeg.log")

    # Wait for first frame
    time.sleep(2)

    # Get container IP
    try:
        hostname = (
            subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        )
        print(f"\n🌐 Open in your browser:")
        print(f"   http://localhost:{web_port}/simple_web_viewer.html")
        print(f"   http://{hostname}:{web_port}/simple_web_viewer.html")
    except:
        print(f"\n🌐 Open in your browser:")
        print(f"   http://localhost:{web_port}/simple_web_viewer.html")

    return {"ffmpeg_pid": ffmpeg_process.pid, "webserver_pid": webserver_process.pid}


def main():
    """Main entry point"""
    print("\n🎥 HammyCam Starting...\n")

    # Load configuration
    config = load_config()

    # Check if auto-start is enabled
    autostart = config.get("autostart", {})
    if not autostart.get("enabled", True):
        print("Auto-start is disabled in config")
        sys.exit(0)

    # Wait for delay
    delay = autostart.get("delay", 2)
    if delay > 0:
        print(f"Waiting {delay} seconds before starting...")
        time.sleep(delay)

    # Start web camera
    pids = start_web_camera(config)

    print("\n" + "=" * 60)
    print("  HammyCam is running!")
    print("=" * 60)
    print(f"\n📹 FFmpeg PID: {pids['ffmpeg_pid']}")
    print(f"📡 Web Server PID: {pids['webserver_pid']}")
    print("\n💡 To stop: scripts/stop_camera.sh")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
