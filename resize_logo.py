#!/usr/bin/env python3
"""
Resize Vaka Sosiale logo to 200x200 pixels for favicon/avatar use.
"""
from PIL import Image
import sys

def resize_logo():
    input_path = "backend/app/static/vaka-sosiale-logo.png"
    output_path = "backend/app/static/vaka-sosiale-logo-200x200.png"
    
    try:
        # Open the image
        img = Image.open(input_path)
        print(f"Original size: {img.size}")
        
        # Resize to 200x200 with high-quality resampling
        # Use LANCZOS for best quality when downscaling
        img_resized = img.resize((200, 200), Image.Resampling.LANCZOS)
        
        # Save the resized image
        img_resized.save(output_path, "PNG", optimize=True)
        
        print(f"✓ Resized logo saved to: {output_path}")
        print(f"New size: {img_resized.size}")
        
        # Print file size
        import os
        size_kb = os.path.getsize(output_path) / 1024
        print(f"File size: {size_kb:.1f} KB")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    resize_logo()
