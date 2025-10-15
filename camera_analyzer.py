#!/usr/bin/env python3
"""
Camera Analyzer - Flexible frame analysis script
Works with fake cameras (test patterns/images) and real cameras

Usage:
    # Use fake camera (reads from web/current_frame.jpg)
    python3 camera_analyzer.py --source fake

    # Use real webcam
    python3 camera_analyzer.py --source webcam

    # Use video file
    python3 camera_analyzer.py --source video --path myvideo.mp4

    # Use static image
    python3 camera_analyzer.py --source image --path images/myimage.jpg
"""

import cv2
import numpy as np
import argparse
import time
from pathlib import Path
from datetime import datetime


class CameraAnalyzer:
    """Flexible camera analyzer that works with multiple source types"""

    def __init__(self, source_type="fake", source_path=None, display=True):
        """
        Initialize the analyzer

        Args:
            source_type: "fake", "webcam", "video", "image"
            source_path: Path to video/image file (if applicable)
            display: Whether to display the video feed
        """
        self.source_type = source_type
        self.source_path = source_path
        self.display = display and self._display_available()
        self.cap = None
        self.frame_count = 0
        self.start_time = time.time()

        self.motion_threshold = 0.30 # 30%

        if display and not self.display:
            print("⚠️  No display available - running in headless mode")
            print("   (Use --no-display to suppress this warning)")

    def _display_available(self):
        """Check if display is available"""
        import os

        # In container environments, DISPLAY might be set but not actually work
        # Just check if we're in a headless environment
        display_env = os.environ.get("DISPLAY", "")

        # If no DISPLAY set, definitely no display
        if not display_env:
            return False

        # Check if we're in a typical container/headless environment
        # This is safer than actually trying cv2.imshow()
        if os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
            # We're in a container - display probably won't work
            return False

        return True

    def connect(self):
        """
        Connect to the camera source
        It will connect to the camera source based on the source type
        and return True if the camera is connected, False otherwise
        Args:
            self: The instance of the class
        Returns:
            True if the camera is connected, False otherwise

        Example:
            analyzer = CameraAnalyzer(source_type="fake")
            analyzer.connect()
        """
        print(f"🎥 Connecting to {self.source_type} camera...")

        if self.source_type == "fake":
            # For fake camera, we'll read the continuously updated file
            self.fake_frame_path = Path("web/current_frame.jpg")
            if not self.fake_frame_path.exists():
                print("❌ Error: Fake camera not running!")
                print("   Run: python3 scripts/start_camera.py")
                return False
            print("✓ Connected to fake camera")
            return True

        elif self.source_type == "webcam":
            # Real webcam (try device 0, 1, 2...)
            for device_id in range(3):
                self.cap = cv2.VideoCapture(device_id)
                if self.cap.isOpened():
                    print(f"✓ Connected to webcam (device {device_id})")
                    return True
            print("❌ Error: No webcam found")
            return False

        elif self.source_type == "video":
            # Video file
            if not self.source_path or not Path(self.source_path).exists():
                print(f"❌ Error: Video file not found: {self.source_path}")
                return False
            self.cap = cv2.VideoCapture(self.source_path)
            if self.cap.isOpened():
                print(f"✓ Connected to video: {self.source_path}")
                return True
            return False

        elif self.source_type == "image":
            # Static image
            if not self.source_path or not Path(self.source_path).exists():
                print(f"❌ Error: Image file not found: {self.source_path}")
                return False
            print(f"✓ Loaded image: {self.source_path}")
            return True

        return False

    def read_frame(self):
        """Read a frame from the source"""
        if self.source_type == "fake":
            # Read the continuously updated file
            if not self.fake_frame_path.exists():
                return False, None
            frame = cv2.imread(str(self.fake_frame_path))
            return frame is not None, frame

        elif self.source_type == "image":
            # Read static image
            frame = cv2.imread(self.source_path)
            return frame is not None, frame

        else:
            # OpenCV VideoCapture (webcam/video)
            return self.cap.read()

    def analyze_frame(self, frame):
        """
        Analyze the frame and detect content

        This is where you'd add your detection logic:
        - Object detection (YOLO, etc.)
        - Face detection
        - Motion detection
        - Color analysis
        - OCR/text detection
        - etc.
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "frame_number": self.frame_count,
        }

        # # Example 1: Basic color analysis
        # avg_color = frame.mean(axis=(0, 1))
        # results["avg_color_bgr"] = avg_color.tolist()
        # results["dominant_color"] = self._get_dominant_color(avg_color)

        # # Example 2: Brightness analysis
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # results["avg_brightness"] = gray.mean()
        # results["brightness_level"] = self._classify_brightness(gray.mean())

        # # Example 3: Simple edge detection (complexity measure)
        # edges = cv2.Canny(gray, 100, 200)
        # edge_pixels = np.count_nonzero(edges)
        # results["edge_pixels"] = int(edge_pixels)
        # results["complexity"] = "high" if edge_pixels > 10000 else "low"

        return results

    def _get_dominant_color(self, avg_color):
        """Classify dominant color"""
        b, g, r = avg_color
        if r > g and r > b:
            return "red"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        elif r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        else:
            return "mixed"

    def _classify_brightness(self, brightness):
        """Classify brightness level"""
        if brightness > 200:
            return "very bright"
        elif brightness > 150:
            return "bright"
        elif brightness > 100:
            return "normal"
        elif brightness > 50:
            return "dim"
        else:
            return "dark"

    def annotate_frame(self, frame, results):
        """Add analysis results as text overlay on frame"""
        annotated = frame.copy()

        # Add text overlay
        y_offset = 30
        font = cv2.FONT_HERSHEY_SIMPLEX

        texts = [
            f"Frame: {results['frame_number']}",
            f"Color: {results['dominant_color']}",
            f"Brightness: {results['brightness_level']}",
            f"Complexity: {results['complexity']}",
        ]

        if results.get("faces_detected") != "N/A":
            texts.append(f"Faces: {results['faces_detected']}")

        for text in texts:
            cv2.putText(annotated, text, (10, y_offset), font, 0.7, (0, 255, 0), 2)
            y_offset += 30

        return annotated

    def run(self, max_frames=None, fps=10, save_interval=None, output_dir="."):
        """
        Run the analyzer

        Args:
            max_frames: Maximum number of frames to process (None = infinite)
            fps: Frames per second to process
            save_interval: Save frame every N frames (None = don't auto-save)
            output_dir: Directory to save frames
        """
        if not self.connect():
            return

        # Create output directory if needed
        if save_interval:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Saving frames to: {output_path.absolute()}")

        print(f"\n{'='*60}")
        print("  Camera Analyzer Running")
        print(f"{'='*60}")
        print(f"Source: {self.source_type}")
        print(f"Display: {'ON' if self.display else 'OFF'}")
        print(f"Max frames: {max_frames if max_frames else 'unlimited'}")
        if save_interval:
            print(f"Auto-save: Every {save_interval} frames")
        if self.display:
            print("\nPress 'q' to quit, 's' to save current frame")
        else:
            print("\nPress Ctrl+C to quit")
        print(f"{'='*60}\n")

        frame_delay = int(1000 / fps)  # milliseconds
        ret, last_frame = self.read_frame()

        try:
            while True:
                # Check frame limit
                if max_frames and self.frame_count >= max_frames:
                    print(f"\n✓ Reached max frames ({max_frames})")
                    break

                # Read frame
                ret, frame = self.read_frame()
                if not ret or frame is None:
                    if self.source_type in ["video", "fake"]:
                        time.sleep(0.1)  # Wait for next frame
                        continue
                    else:
                        print("❌ Failed to read frame")
                        break

                motion_detected = self.was_motion_detected(frame, last_frame)
                if motion_detected:
                    print("Motion detected")

                self.frame_count += 1
                last_frame = frame

                '''Handling testing environment below this line'''
                # Auto-save frames if interval specified
                if save_interval and self.frame_count % save_interval == 0:
                    # annotated = self.annotate_frame(frame, results)
                    filename = (
                        Path(output_dir)
                        / f"frame_{self.frame_count:06d}_{datetime.now().strftime('%H%M%S')}.jpg"
                    )
                    cv2.imwrite(str(filename), annotated)
                    print(f"💾 Saved: {filename}")

                # Add small delay for fake camera to avoid reading same frame
                if self.source_type in ["fake", "image"]:
                    time.sleep(1.0 / fps)

        except KeyboardInterrupt:
            print("\n\n✓ Interrupted by user")

        finally:
            self.cleanup()
            self.print_summary()

    def was_motion_detected(self, frame, last_frame):
        """Detect motion in the frame"""

        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)

        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        changed_pixels = np.count_nonzero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        change_percent = (changed_pixels / total_pixels) * 100

        return change_percent >= self.motion_threshold

    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        if self.display:
            cv2.destroyAllWindows()

    def print_summary(self):
        """Print analysis summary"""
        elapsed = time.time() - self.start_time
        avg_fps = self.frame_count / elapsed if elapsed > 0 else 0

        print(f"\n{'='*60}")
        print("  Analysis Summary")
        print(f"{'='*60}")
        print(f"Total frames: {self.frame_count}")
        print(f"Total time: {elapsed:.1f}s")
        print(f"Average FPS: {avg_fps:.1f}")
        print(f"{'='*60}\n")


def main():

    # Handling arguments for the software to run
    parser = argparse.ArgumentParser(description="Flexible Camera Analyzer")
    parser.add_argument(
        "--source",
        choices=["fake", "webcam", "video", "image"],
        default="fake",
        help="Camera source type",
    )
    parser.add_argument("--path", type=str, help="Path to video/image file")
    parser.add_argument(
        "--no-display", action="store_true", help="Disable video display"
    )
    parser.add_argument("--max-frames", type=int, help="Maximum frames to process")
    parser.add_argument(
        "--fps", type=int, default=10, help="Frames per second to process (default: 10)"
    )
    parser.add_argument(
        "--save-interval",
        type=int,
        help="Save annotated frame every N frames (e.g., 30 = every 30 frames)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save frames (default: current)",
    )

    args = parser.parse_args()

    # Creating the analyzer with the given arguments
    analyzer = CameraAnalyzer(
        source_type=args.source, source_path=args.path, display=not args.no_display
    )

    # Running the analyzer on the camera
    analyzer.run(
        max_frames=args.max_frames,
        fps=args.fps,
        save_interval=args.save_interval,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
