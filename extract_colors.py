#!/usr/bin/env python3
"""
Color Palette Extraction Utility for Minecraft Map Art Ditherer
Supports multiple palette formats: ACT, PNG, TXT, and manual extraction
"""

import struct
from PIL import Image
import re

def extract_from_act_file(act_file_path):
    """Extract colors from Adobe Color Table (.act) file"""
    colors = []
    try:
        with open(act_file_path, 'rb') as f:
            # ACT files contain 256 RGB triplets (768 bytes total)
            data = f.read(768)
            for i in range(0, len(data), 3):
                if i + 2 < len(data):
                    r, g, b = struct.unpack('BBB', data[i:i+3])
                    hex_color = f"#{r:02X}{g:02X}{b:02X}"
                    colors.append(hex_color)
    except Exception as e:
        print(f"Error reading ACT file: {e}")
    
    # Remove duplicates while preserving order
    unique_colors = []
    seen = set()
    for color in colors:
        if color not in seen:
            unique_colors.append(color)
            seen.add(color)
    
    return unique_colors

def extract_from_png_palette(png_file_path):
    """Extract colors from PNG image palette"""
    colors = []
    try:
        img = Image.open(png_file_path)
        if img.mode == 'P':  # Palette mode
            palette = img.getpalette()
            if palette:
                for i in range(0, len(palette), 3):
                    if i + 2 < len(palette):
                        r, g, b = palette[i], palette[i+1], palette[i+2]
                        hex_color = f"#{r:02X}{g:02X}{b:02X}"
                        colors.append(hex_color)
        else:
            # Extract unique colors from image
            img = img.convert('RGB')
            unique_colors = set()
            for pixel in img.getdata():
                r, g, b = pixel
                hex_color = f"#{r:02X}{g:02X}{b:02X}"
                unique_colors.add(hex_color)
            colors = list(unique_colors)
    except Exception as e:
        print(f"Error reading PNG file: {e}")
    
    # Remove duplicates while preserving order (for palette mode)
    if colors:
        unique_colors = []
        seen = set()
        for color in colors:
            if color not in seen:
                unique_colors.append(color)
                seen.add(color)
        colors = unique_colors
    
    return colors

def extract_from_text_file(text_file_path):
    """Extract hex colors from text file (various formats)"""
    colors = []
    hex_pattern = re.compile(r'#?([0-9A-Fa-f]{6})')
    
    try:
        with open(text_file_path, 'r') as f:
            content = f.read()
            matches = hex_pattern.findall(content)
            colors = [f"#{match.upper()}" for match in matches]
    except Exception as e:
        print(f"Error reading text file: {e}")
    
    # Remove duplicates while preserving order
    unique_colors = []
    seen = set()
    for color in colors:
        if color not in seen:
            unique_colors.append(color)
            seen.add(color)
    
    return unique_colors

def minecraft_carpet_colors():
    """
    Minecraft Java Edition carpet colors for flat map art
    Based on research from Minecraft Wiki and color palette databases
    """
    return [
        # From the 2D palette research - 61 colors for flat map art
        "#DC0000", "#A3292A", "#842C2C", "#8A4243", "#7A3327", "#600100", "#4F1519",
        "#BA6D2C", "#A0721F", "#89461F", "#6F4A2A", "#7B663E", "#58412C", "#825E42",
        "#745C54", "#B4988A", "#BA967E", "#D5C98C", "#C5C52C", "#D7CD42", "#6D9930",
        "#6DB015", "#58642D", "#586D2C", "#414624", "#006A00", "#00BB32", "#6D9081",
        "#119B72", "#327A78", "#126C73", "#416D84", "#5884BA", "#3F6EDC", "#3737DC",
        "#2C4199", "#4FBCB7", "#8A8ADC", "#8D909E", "#605D77", "#41354F", "#9941BA",
        "#6D3699", "#D06D8E", "#7F3653", "#804B5D", "#693E4B", "#4A2535", "#DCDCDC",
        "#DCD9D3", "#ABABAB", "#909090", "#848484", "#606060", "#565656", "#4B4F4F",
        "#414141", "#151515", "#1F120D", "#31231E", "#412B1E"
    ]

def save_colors_to_file(colors, output_file):
    """Save extracted colors to a Python file for use in the ditherer"""
    with open(output_file, 'w') as f:
        f.write('"""Minecraft Carpet Color Palette for Map Art Dithering"""\n\n')
        f.write('MINECRAFT_CARPET_COLORS = [\n')
        for i, color in enumerate(colors):
            f.write(f'    "{color}",  # Color {i+1}\n')
        f.write(']\n\n')
        f.write(f'# Total colors: {len(colors)}\n')

def main():
    print("Minecraft Map Art Ditherer - Color Palette Extractor")
    print("=" * 50)
    
    # Option 1: Use researched Minecraft colors
    print("Option 1: Use researched Minecraft carpet colors (recommended)")
    minecraft_colors = minecraft_carpet_colors()
    print(f"Found {len(minecraft_colors)} Minecraft carpet colors")
    
    # Save the researched colors
    save_colors_to_file(minecraft_colors, 'minecraft_colors.py')
    print("✅ Saved researched colors to 'minecraft_colors.py'")
    
    # Option 2: Extract from user file
    print("\nOption 2: Extract from your palette file")
    print("Supported formats: .act, .png, .txt")
    
    file_path = input("Enter path to your palette file (or press Enter to skip): ").strip()
    
    if file_path:
        if file_path.lower().endswith('.act'):
            colors = extract_from_act_file(file_path)
        elif file_path.lower().endswith('.png'):
            colors = extract_from_png_palette(file_path)
        elif file_path.lower().endswith('.txt'):
            colors = extract_from_text_file(file_path)
        else:
            print("Unsupported file format")
            return
        
        if colors:
            # Count original vs unique colors for user feedback
            original_count = len(colors)
            
            # Additional deduplication check (in case extraction methods missed any)
            final_colors = []
            seen = set()
            for color in colors:
                if color not in seen:
                    final_colors.append(color)
                    seen.add(color)
            
            unique_count = len(final_colors)
            duplicates_removed = original_count - unique_count
            
            print(f"✅ Extracted {unique_count} unique colors from {file_path}")
            if duplicates_removed > 0:
                print(f"   (Removed {duplicates_removed} duplicate entries)")
            
            save_colors_to_file(final_colors, 'extracted_colors.py')
            print("✅ Saved extracted colors to 'extracted_colors.py'")
            
            # Show first 10 colors as preview
            print("\nPreview of extracted colors:")
            for i, color in enumerate(final_colors[:10]):
                print(f"  {i+1}: {color}")
            if len(final_colors) > 10:
                print(f"  ... and {len(final_colors) - 10} more")
        else:
            print("❌ No colors found in the file")

if __name__ == "__main__":
    main() 