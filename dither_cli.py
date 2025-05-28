#!/usr/bin/env python3
"""
Command-Line Interface for Minecraft Map Art Ditherer
Test the dithering algorithm with real images
"""

import argparse
import sys
import os
import time
from pathlib import Path

# Add src directory to path
sys.path.append('src')

from dithering import MinecraftDitherer
from image_utils import ImageProcessor
from PIL import Image

def progress_callback(current, total):
    """Progress callback for dithering"""
    percent = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r🔄 Progress: |{bar}| {percent:.1f}% ({current}/{total} pixels)', end='', flush=True)
    
    if current == total:
        print()  # New line when complete

def load_custom_palette():
    """Load custom palette if available"""
    try:
        from minecraft_colors import MINECRAFT_CARPET_COLORS
        return MINECRAFT_CARPET_COLORS
    except ImportError:
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Minecraft Map Art Ditherer - Convert images to dithered map art',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dither_cli.py input.jpg                    # Basic dithering
  python dither_cli.py input.png -o output.png      # Specify output
  python dither_cli.py input.jpg --no-resize        # Don't resize to 128x128
  python dither_cli.py input.jpg --comparison       # Save comparison images
  python dither_cli.py --palette-preview            # Generate palette preview
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input image file')
    parser.add_argument('-o', '--output', help='Output file path (default: input_dithered.png)')
    parser.add_argument('--no-resize', action='store_true', help='Don\'t resize to Minecraft map size (128x128)')
    parser.add_argument('--comparison', action='store_true', help='Save original, quantized, and dithered versions')
    parser.add_argument('--palette-preview', action='store_true', help='Generate and save palette preview')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress output')
    
    args = parser.parse_args()
    
    # Handle palette preview
    if args.palette_preview:
        print("🎨 Generating palette preview...")
        custom_colors = load_custom_palette()
        ditherer = MinecraftDitherer(custom_colors)
        
        if ditherer.save_palette_preview("palette_preview.png"):
            print("✅ Palette preview saved as 'palette_preview.png'")
        return
    
    # Validate input
    if not args.input:
        parser.error("Input image file is required (unless using --palette-preview)")
    
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found")
        return 1
    
    if not ImageProcessor.is_supported_format(args.input):
        print(f"❌ Error: Unsupported file format. Supported: {', '.join(ImageProcessor.SUPPORTED_FORMATS)}")
        return 1
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_dithered.png"
    
    print("🚀 Minecraft Map Art Ditherer")
    print("=" * 40)
    
    # Load custom palette
    custom_colors = load_custom_palette()
    if custom_colors:
        print(f"📦 Using custom palette with {len(custom_colors)} colors")
    else:
        print("📦 Using default 61-color palette")
    
    # Initialize ditherer
    ditherer = MinecraftDitherer(custom_colors)
    
    # Set progress callback
    if not args.quiet:
        ditherer.set_progress_callback(progress_callback)
    
    # Load image
    print(f"📂 Loading image: {args.input}")
    image = ImageProcessor.load_image(args.input)
    
    if image is None:
        print("❌ Failed to load image")
        return 1
    
    print(f"📊 Original image: {image.size[0]}x{image.size[1]} pixels")
    
    # Start timing
    start_time = time.time()
    
    try:
        if args.comparison:
            # Generate comparison images
            print("🔄 Generating comparison images...")
            original, quantized, dithered = ditherer.dither_with_comparison(
                image, 
                resize_for_minecraft=not args.no_resize
            )
            
            # Save all versions
            base_path = Path(output_path)
            original_path = base_path.parent / f"{base_path.stem}_original.png"
            quantized_path = base_path.parent / f"{base_path.stem}_quantized.png"
            dithered_path = output_path
            
            original.save(original_path)
            quantized.save(quantized_path)
            dithered.save(dithered_path)
            
            print(f"✅ Saved original: {original_path}")
            print(f"✅ Saved quantized: {quantized_path}")
            print(f"✅ Saved dithered: {dithered_path}")
            
        else:
            # Standard dithering
            dithered = ditherer.dither_image(image, resize_for_minecraft=not args.no_resize)
            
            # Save result
            ImageProcessor.save_image(dithered, str(output_path))
            print(f"✅ Saved dithered image: {output_path}")
    
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        return 1
    
    # Show timing
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"⏱️  Processing time: {processing_time:.2f} seconds")
    
    # Show palette info
    info = ditherer.get_palette_info()
    print(f"🎨 Used {info['color_count']} colors with {info['algorithm']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 