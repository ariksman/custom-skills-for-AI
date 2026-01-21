#!/usr/bin/env python3
"""
AI-powered background removal using rembg.

This is the FALLBACK method when the two-pass technique isn't feasible
(e.g., when generating images without seed control).

Usage:
    python remove_background.py <input_image> <output_png>

Example:
    python remove_background.py logo.webp logo_transparent.png

Requirements:
    pip install rembg[gpu]  # For GPU acceleration
    # or
    pip install rembg       # CPU-only
"""

import argparse
import sys
from pathlib import Path

try:
    from rembg import remove
    from PIL import Image
except ImportError as e:
    if 'rembg' in str(e):
        print("Error: rembg is required. Install with: pip install rembg")
    else:
        print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


def remove_background(input_path: str, output_path: str) -> None:
    """
    Remove background from an image using AI (U2-Net model).
    
    Args:
        input_path: Path to input image (any format)
        output_path: Path for output PNG with alpha channel
    """
    # Load input image
    input_image = Image.open(input_path)
    
    # Remove background using rembg
    output_image = remove(input_image)
    
    # Save as PNG (preserves alpha)
    output_image.save(output_path, 'PNG')
    print(f"✅ Saved transparent image to: {output_path}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Remove background from an image using AI.",
        epilog="Uses the U2-Net model via rembg for accurate edge detection."
    )
    parser.add_argument(
        "input",
        help="Path to input image (supports most formats)"
    )
    parser.add_argument(
        "output",
        help="Output path for PNG with transparent background"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Run removal
    remove_background(args.input, args.output)


if __name__ == "__main__":
    main()
