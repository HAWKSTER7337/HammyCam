#!/usr/bin/env python3
"""
Process images with timestamp overlay - No virtual camera needed
Saves the output to a file that you can use anywhere
"""

import cv2
import argparse
from datetime import datetime
import os


def main():
    parser = argparse.ArgumentParser(description="Process Image with Overlay")
    parser.add_argument("--image", type=str, required=True, help="Input image path")
    parser.add_argument(
        "--output", type=str, default="output.jpg", help="Output image path"
    )
    parser.add_argument(
        "--width", type=int, default=1280, help="Output width (default: 1280)"
    )
    parser.add_argument(
        "--height", type=int, default=720, help="Output height (default: 720)"
    )
    parser.add_argument("--text", type=str, help="Custom text to display (optional)")
    args = parser.parse_args()

    # Load the image
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        return

    image = cv2.imread(args.image)
    if image is None:
        print(f"Error: Could not load image: {args.image}")
        return

    print(f"Loaded image: {args.image}")
    print(f"Original size: {image.shape[1]}x{image.shape[0]}")

    # Resize image
    resized_image = cv2.resize(image, (args.width, args.height))

    # Add timestamp overlay
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        resized_image,
        timestamp,
        (10, args.height - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

    # Add custom text if provided
    if args.text:
        cv2.putText(
            resized_image,
            args.text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

    # Save the output
    cv2.imwrite(args.output, resized_image)
    print(f"Saved processed image to: {args.output}")
    print(f"Output size: {args.width}x{args.height}")


if __name__ == "__main__":
    main()
