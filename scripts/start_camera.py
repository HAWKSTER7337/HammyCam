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
    """Start the web camera"""
    camera = config["camera"]
    display_config = config.get("display", {})
    
    mode = camera["mode"]
    width = camera["width"]
    height = camera["height"]
    fps = camera["fps"]
    web_port = display_config.get("web_port", 8080)
    
    print("=" * 60)
    print("  HammyCam Web Camera")
    print("=" * 60)
    print(f"Mode: {mode}")
    print(f"Resolution: {width}x{height} @ {fps}fps")
    print(f"Web Port: {web_port}")
    print("=" * 60)

    # Build command
    script_dir = Path(__file__).parent
    if mode == "image":
        image_path = camera.get("image_path", "images/black.jpg")
        cmd = [
            str(script_dir / "simple_web_camera.sh"),
            str(script_dir.parent / image_path),
            str(width),
            str(height),
            str(fps),
            str(web_port),
        ]
    else:  # test_pattern
        cmd = [
            str(script_dir / "simple_web_camera.sh"),
            "",  # Empty for test pattern
            str(width),
            str(height),
            str(fps),
            str(web_port),
        ]

    # Start in background
    log_file = open("/tmp/hammycam_web.log", "w")
    process = subprocess.Popen(
        cmd, stdout=log_file, stderr=subprocess.STDOUT, cwd=script_dir.parent
    )

    print(f"✓ Web camera started (PID: {process.pid})")
    print(f"  Logs: /tmp/hammycam_web.log")

    # Save PID
    pid_file = Path("/tmp/hammycam_web.pid")
    pid_file.write_text(str(process.pid))

    # Wait for server to start
    time.sleep(3)
    
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

    return process.pid




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
    web_pid = start_web_camera(config)

    print("\n" + "=" * 60)
    print("  HammyCam is running!")
    print("=" * 60)
    print("\n💡 To stop: ./stop_camera.sh")
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
