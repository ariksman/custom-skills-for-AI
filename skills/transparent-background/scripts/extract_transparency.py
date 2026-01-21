#!/usr/bin/env python3
"""
Two-Pass Alpha Extraction for Transparent Background Images.

This script extracts true alpha transparency from two images of the same subject:
one rendered on a pure white background and one on a pure black background.

Algorithm based on: https://jidefr.medium.com/generating-transparent-background-images-with-nano-banana-pro-2-1866c88a33c5

Usage:
    python extract_transparency.py <image_on_white> <image_on_black> <output_png>

Example:
    python extract_transparency.py icon_white.webp icon_black.webp icon_transparent.png
"""

import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


def extract_alpha_two_pass(
    img_on_white_path: str,
    img_on_black_path: str,
    output_path: str,
    alpha_threshold: float = 0.01
) -> None:
    """
    Extract true alpha transparency using the two-pass technique.
    
    The algorithm works by comparing how each pixel appears on white vs black backgrounds:
    - Fully opaque pixels look identical on both backgrounds (distance = 0)
    - Fully transparent pixels look exactly like the background (distance = max)
    - Semi-transparent pixels fall somewhere in between
    
    Args:
        img_on_white_path: Path to image rendered on pure white (#FFFFFF) background
        img_on_black_path: Path to image rendered on pure black (#000000) background
        output_path: Path for output PNG with true alpha channel
        alpha_threshold: Minimum alpha value to consider for color recovery (default: 0.01)
    """
    # Load images
    img_white = Image.open(img_on_white_path).convert('RGBA')
    img_black = Image.open(img_on_black_path).convert('RGBA')
    
    # Validate dimensions match
    if img_white.size != img_black.size:
        raise ValueError(
            f"Dimension mismatch: white bg image is {img_white.size}, "
            f"black bg image is {img_black.size}. Images must be identical size."
        )
    
    width, height = img_white.size
    
    # Get pixel data
    pixels_white = img_white.load()
    pixels_black = img_black.load()
    
    # Create output image
    output = Image.new('RGBA', (width, height))
    pixels_out = output.load()
    
    # Distance between White (255,255,255) and Black (0,0,0)
    # sqrt(255^2 + 255^2 + 255^2) ≈ 441.67
    bg_dist = math.sqrt(3 * 255 * 255)
    
    for y in range(height):
        for x in range(width):
            # Get RGB values from both images
            r_w, g_w, b_w, _ = pixels_white[x, y]
            r_b, g_b, b_b, _ = pixels_black[x, y]
            
            # Calculate Euclidean distance between the two observed colors
            pixel_dist = math.sqrt(
                (r_w - r_b) ** 2 +
                (g_w - g_b) ** 2 +
                (b_w - b_b) ** 2
            )
            
            # THE FORMULA:
            # If pixel is 100% opaque: looks same on both backgrounds (pixel_dist = 0) → alpha = 1
            # If pixel is 100% transparent: looks like backgrounds (pixel_dist = bg_dist) → alpha = 0
            alpha = 1.0 - (pixel_dist / bg_dist)
            
            # Clamp to valid range
            alpha = max(0.0, min(1.0, alpha))
            
            # Color Recovery:
            # Use the image on black to recover the foreground color
            # Since BG is black (0,0,0), the formula C / alpha gives us the original color
            if alpha > alpha_threshold:
                # Un-premultiply to recover true foreground color
                r_out = min(255, int(r_b / alpha))
                g_out = min(255, int(g_b / alpha))
                b_out = min(255, int(b_b / alpha))
            else:
                # Near-transparent pixels: color doesn't matter
                r_out = g_out = b_out = 0
            
            # Set output pixel
            pixels_out[x, y] = (r_out, g_out, b_out, int(alpha * 255))
    
    # Save as PNG (preserves alpha)
    output.save(output_path, 'PNG')
    print(f"✅ Saved transparent image to: {output_path}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract true alpha transparency using two-pass technique.",
        epilog="Generate two images with identical content: one on white, one on black background."
    )
    parser.add_argument(
        "image_on_white",
        help="Path to image rendered on pure white background"
    )
    parser.add_argument(
        "image_on_black", 
        help="Path to image rendered on pure black background"
    )
    parser.add_argument(
        "output",
        help="Output path for PNG with true alpha channel"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.01,
        help="Alpha threshold for color recovery (default: 0.01)"
    )
    
    args = parser.parse_args()
    
    # Validate input files exist
    for path in [args.image_on_white, args.image_on_black]:
        if not Path(path).exists():
            print(f"Error: File not found: {path}")
            sys.exit(1)
    
    # Run extraction
    extract_alpha_two_pass(
        args.image_on_white,
        args.image_on_black,
        args.output,
        args.threshold
    )


if __name__ == "__main__":
    main()
