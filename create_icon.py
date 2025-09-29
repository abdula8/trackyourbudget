#!/usr/bin/env python3
"""
Create a simple icon for a Budget Calculator application.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """Create a simple icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ PIL (Pillow) not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
    
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background circle with a green fill
    margin = 20
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(46, 204, 113, 255),    # a pleasant green color
        outline=(39, 174, 96, 255),  # darker green outline
        width=4
    )
    
    # Draw a simple checkmark symbol for the calculator
    # Coordinates are calculated to center the checkmark
    checkmark_points = [
        (size * 0.25, size * 0.5),    # bottom left
        (size * 0.45, size * 0.7),    # corner point
        (size * 0.75, size * 0.35),   # top right
    ]
    draw.line(checkmark_points, fill=(255, 255, 255, 255), width=20, joint="bevel")
    
    # Add text "BC"
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
        except:
            font = ImageFont.load_default()
    
    text = "BC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = size - margin - text_height - 10
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO
    img.save("icon.ico", format='ICO',
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✅ Icon created: icon.ico")
    
    # Also save as PNG for reference
    img.save("icon.png", format='PNG')
    print("✅ Icon reference: icon.png")

if __name__ == "__main__":
    import sys
    create_icon()
