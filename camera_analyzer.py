import cv2
import numpy as np
import subprocess
import time
from pathlib import Path
from datetime import datetime
import tempfile
import os

def read_frame(self):
    """Capture a single frame via libcamera-still using a temp file"""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "libcamera-still",
        "-n",              # no preview
        "--immediate",     # capture instantly
        "--width", "640",
        "--height", "480",
        "-o", tmp_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        frame = cv2.imread(tmp_path)
        os.remove(tmp_path)
        if frame is None:
            return False, None
        return True, frame
    except subprocess.CalledProcessError:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False, None

class CameraAnalyzer:
    """Camera analyzer using libcamera-still (Bookworm compatible)"""

    def __init__(self, display=True):
        self.display = display
        self.frame_count = 0
        self.start_time = time.time()
        self.motion_threshold = 0.30  # percent difference threshold

    def connect(self):
        """Test if libcamera works"""
        print("🎥 Checking libcamera access...")
        try:
            subprocess.run(
                ["libcamera-still", "-n", "--immediate", "-o", "/dev/null"],  check=True)
            print("✓ Camera ready (libcamera-still)")
            return True
        except subprocess.CalledProcessError:
            print("❌ libcamera-still failed to capture a frame")
            return False

    def read_frame(self):
        """Capture a single frame via libcamera-still using a temp file"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
    
        cmd = [
            "libcamera-still",
            "-n",              # no preview
            "--immediate",     # capture instantly
            "--width", "640",
            "--height", "480",
            "-o", tmp_path
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            frame = cv2.imread(tmp_path)
            os.remove(tmp_path)
            if frame is None:
                return False, None
            return True, frame
        except subprocess.CalledProcessError:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return False, None

    def was_motion_detected(self, frame, last_frame):
        """Detect motion between two frames"""
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        changed_pixels = np.count_nonzero(thresh)
        total_pixels = thresh.size
        change_percent = (changed_pixels / total_pixels) * 100
        return change_percent >= self.motion_threshold

    def run(self, fps=1, max_frames=None):
        """Run the analyzer loop"""
        if not self.connect():
            return

        print("\n🚀 Running live camera analysis (libcamera)\n")
        last_frame = None

        try:
            while True:
                if max_frames and self.frame_count >= max_frames:
                    break

                ret, frame = self.read_frame()
                if not ret or frame is None:
                    print("⚠️ Failed to read frame")
                    time.sleep(1)
                    continue

                if last_frame is not None and self.was_motion_detected(frame, last_frame):
                    print(f"🟠 Motion detected (frame {self.frame_count})")

                self.frame_count += 1
                last_frame = frame

                if self.display:
                    cv2.imshow("Camera Analyzer", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                time.sleep(1.0 / fps)

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")

        finally:
            cv2.destroyAllWindows()
            self.print_summary()

    def print_summary(self):
        elapsed = time.time() - self.start_time
        avg_fps = self.frame_count / elapsed if elapsed > 0 else 0
        print(f"\n📊 Summary: {self.frame_count} frames in {elapsed:.1f}s ({avg_fps:.2f} FPS)")

if __name__ == "__main__":
    analyzer = CameraAnalyzer(display=False)
    analyzer.run(fps=1)
