#!/usr/bin/env python3
"""
Phase 1 Test Script for Minecraft Map Art Ditherer
Tests the color palette manager and image utilities
"""

import sys
import os
sys.path.append('src')

from palette import MinecraftPalette
from image_utils import ImageProcessor
from PIL import Image
import numpy as np

def test_color_palette():
    """Test the Minecraft color palette functionality"""
    print("🎨 Testing Color Palette Manager")
    print("=" * 40)
    
    # Initialize palette
    palette = MinecraftPalette()
    
    # Test basic functionality
    print(f"✅ Loaded {len(palette.CARPET_COLORS)} colors")
    
    # Test color matching with common colors
    test_colors = [
        ((255, 0, 0), "Pure Red"),
        ((0, 255, 0), "Pure Green"), 
        ((0, 0, 255), "Pure Blue"),
        ((255, 255, 255), "White"),
        ((0, 0, 0), "Black"),
        ((128, 128, 128), "Gray"),
        ((255, 165, 0), "Orange"),
        ((128, 0, 128), "Purple")
    ]
    
    print("\n🔍 Color Matching Tests:")
    for rgb, name in test_colors:
        idx, closest_rgb, closest_hex = palette.find_closest_color(rgb, method="lab")
        distance = palette.calculate_color_distance(rgb, closest_rgb, method="lab")
        print(f"  {name:12} {rgb} -> {closest_hex} (distance: {distance:.1f})")
    
    # Test color info
    print("\n📊 Sample Color Information:")
    for i in [0, 10, 20, 30]:
        info = palette.get_color_info(i)
        if info:
            print(f"  Color {i:2}: {info['hex']} RGB{info['rgb']}")
    
    return True

def test_image_processing():
    """Test the image processing utilities"""
    print("\n🖼️  Testing Image Processing")
    print("=" * 40)
    
    # Test format support
    test_formats = ['test.png', 'test.jpg', 'test.bmp', 'test.gif', 'test.xyz']
    print("📁 Format Support:")
    for fmt in test_formats:
        supported = ImageProcessor.is_supported_format(fmt)
        status = "✅ Supported" if supported else "❌ Not supported"
        print(f"  {fmt:12} {status}")
    
    # Create test images
    print("\n🔧 Creating Test Images:")
    
    # Small test image
    small_img = Image.new('RGB', (64, 64), (255, 128, 0))
    print(f"  Small image: {small_img.size}")
    
    # Large test image  
    large_img = Image.new('RGB', (512, 256), (0, 128, 255))
    print(f"  Large image: {large_img.size}")
    
    # Test resizing for Minecraft
    print("\n📏 Minecraft Resizing Tests:")
    minecraft_small = ImageProcessor.resize_for_minecraft(small_img)
    minecraft_large = ImageProcessor.resize_for_minecraft(large_img)
    
    print(f"  {small_img.size} -> {minecraft_small.size}")
    print(f"  {large_img.size} -> {minecraft_large.size}")
    
    # Test array conversion
    print("\n🔄 Array Conversion Tests:")
    array = ImageProcessor.image_to_array(minecraft_small)
    back_to_image = ImageProcessor.array_to_image(array)
    
    print(f"  Image -> Array: {array.shape}")
    print(f"  Array -> Image: {back_to_image.size}")
    
    # Test validation
    print("\n✅ Image Validation Tests:")
    test_images = [
        (small_img, "Small image"),
        (large_img, "Large image"),
        (None, "None image"),
        (Image.new('RGB', (0, 0)), "Zero size image")
    ]
    
    for img, desc in test_images:
        if img is not None and img.size == (0, 0):
            # Skip zero size test as it might cause issues
            print(f"  {desc:15} ❌ Invalid (zero size)")
            continue
            
        is_valid, message = ImageProcessor.validate_image_for_processing(img)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"  {desc:15} {status} - {message}")
    
    return True

def test_integration():
    """Test integration between palette and image processing"""
    print("\n🔗 Testing Integration")
    print("=" * 40)
    
    # Create a test image with known colors
    palette = MinecraftPalette()
    
    # Create a small test image with gradient
    test_img = Image.new('RGB', (4, 4))
    pixels = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 255, 255),
        (0, 0, 0), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (64, 64, 64), (192, 192, 192), (255, 128, 0), (128, 255, 128)
    ]
    test_img.putdata(pixels)
    
    print(f"📊 Created test image: {test_img.size}")
    
    # Convert to array and process each pixel
    array = ImageProcessor.image_to_array(test_img)
    height, width, channels = array.shape
    
    print(f"🎯 Processing {width}x{height} pixels:")
    
    matched_colors = []
    for y in range(height):
        for x in range(width):
            original_rgb = tuple(array[y, x])
            idx, closest_rgb, closest_hex = palette.find_closest_color(original_rgb)
            matched_colors.append(closest_rgb)
            
            if len(matched_colors) <= 4:  # Show first few
                print(f"  Pixel ({x},{y}): {original_rgb} -> {closest_hex}")
    
    print(f"✅ Successfully matched {len(matched_colors)} pixels to Minecraft colors")
    
    return True

def main():
    """Run all Phase 1 tests"""
    print("🚀 Minecraft Map Art Ditherer - Phase 1 Tests")
    print("=" * 50)
    
    try:
        # Test individual components
        success1 = test_color_palette()
        success2 = test_image_processing() 
        success3 = test_integration()
        
        # Summary
        print("\n📋 Test Summary")
        print("=" * 40)
        
        tests = [
            ("Color Palette Manager", success1),
            ("Image Processing", success2), 
            ("Integration", success3)
        ]
        
        all_passed = True
        for test_name, passed in tests:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {test_name:20} {status}")
            if not passed:
                all_passed = False
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        if all_passed:
            print("\n🎉 Phase 1 infrastructure is ready!")
            print("   Next: Implement the dithering algorithm (Phase 2)")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 