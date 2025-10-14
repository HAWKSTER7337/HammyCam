#!/usr/bin/env python3
"""
Simple Motion Detection Example for HammyCam
This script demonstrates basic motion detection using OpenCV.
"""

import cv2
import numpy as np
from datetime import datetime


class MotionDetector:
    def __init__(self, camera_index=0, threshold=25, min_area=500):
        """
        Initialize the motion detector.
        
        Args:
            camera_index: Camera device index (default: 0)
            threshold: Threshold for motion detection sensitivity (default: 25)
            min_area: Minimum area to consider as motion (default: 500)
        """
        self.camera_index = camera_index
        self.threshold = threshold
        self.min_area = min_area
        self.previous_frame = None
        
    def start(self):
        """Start the motion detection."""
        print("Starting HammyCam Motion Detector...")
        print(f"Camera: {self.camera_index}")
        print(f"Threshold: {self.threshold}")
        print(f"Minimum Area: {self.min_area}")
        print("\nPress 'q' to quit, 's' to save snapshot")
        
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        # Set camera properties (optional)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        motion_detected = False
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Can't receive frame")
                break
            
            frame_count += 1
            
            # Process frame for motion detection
            motion_detected, processed_frame = self.detect_motion(frame)
            
            # Add status text
            status_text = "MOTION DETECTED!" if motion_detected else "No Motion"
            color = (0, 0, 255) if motion_detected else (0, 255, 0)
            cv2.putText(processed_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Add frame counter
            cv2.putText(processed_frame, f"Frame: {frame_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display the frame
            cv2.imshow('HammyCam - Motion Detector', processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"snapshot_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Snapshot saved: {filename}")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released. Goodbye!")
    
    def detect_motion(self, frame):
        """
        Detect motion in the current frame.
        
        Args:
            frame: Current frame from camera
            
        Returns:
            tuple: (motion_detected: bool, processed_frame: np.array)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize the previous frame if needed
        if self.previous_frame is None:
            self.previous_frame = gray
            return False, frame
        
        # Compute absolute difference between current and previous frame
        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate the threshold image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        
        # Loop over the contours
        for contour in contours:
            # Ignore small contours
            if cv2.contourArea(contour) < self.min_area:
                continue
            
            motion_detected = True
            
            # Draw bounding box around motion
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Update previous frame
        self.previous_frame = gray
        
        return motion_detected, frame


def main():
    """Main entry point."""
    # Create motion detector with default settings
    detector = MotionDetector(
        camera_index=0,
        threshold=25,
        min_area=500
    )
    
    # Start detection
    detector.start()


if __name__ == "__main__":
    main()

