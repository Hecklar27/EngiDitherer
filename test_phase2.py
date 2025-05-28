#!/usr/bin/env python3
"""
Phase 2 Test Script for Minecraft Map Art Ditherer
Tests the dithering algorithm and command-line interface
"""

import sys
import os
import time
from pathlib import Path

# Add src directory to path
sys.path.append('src')

from dithering import MinecraftDitherer
from image_utils import ImageProcessor
from PIL import Image
import numpy as np

def create_test_images():
    """Create various test images for dithering tests"""
    test_images = {}
    
    # 1. Gradient test image
    gradient = Image.new('RGB', (64, 64))
    for y in range(64):
        for x in range(64):
            r = int((x / 63) * 255)
            g = int((y / 63) * 255)
            b = 128
            gradient.putpixel((x, y), (r, g, b))
    test_images['gradient'] = gradient
    
    # 2. Color bands test
    bands = Image.new('RGB', (64, 64))
    for y in range(64):
        for x in range(64):
            if x < 16:
                color = (255, 0, 0)  # Red
            elif x < 32:
                color = (0, 255, 0)  # Green
            elif x < 48:
                color = (0, 0, 255)  # Blue
            else:
                color = (255, 255, 255)  # White
            bands.putpixel((x, y), color)
    test_images['bands'] = bands
    
    # 3. Checkerboard pattern
    checker = Image.new('RGB', (64, 64))
    for y in range(64):
        for x in range(64):
            if (x // 8 + y // 8) % 2 == 0:
                color = (0, 0, 0)  # Black
            else:
                color = (255, 255, 255)  # White
            checker.putpixel((x, y), color)
    test_images['checkerboard'] = checker
    
    # 4. Circular gradient
    circle = Image.new('RGB', (64, 64))
    center_x, center_y = 32, 32
    max_distance = 32
    
    for y in range(64):
        for x in range(64):
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            intensity = max(0, min(255, int(255 * (1 - distance / max_distance))))
            color = (intensity, intensity // 2, 255 - intensity)
            circle.putpixel((x, y), color)
    test_images['circle'] = circle
    
    return test_images

def test_custom_palette_loading():
    """Test loading of custom 16-color palette"""
    print("🎨 Testing Custom Palette Loading")
    print("=" * 40)
    
    try:
        from minecraft_colors import MINECRAFT_CARPET_COLORS
        custom_colors = MINECRAFT_CARPET_COLORS
        print(f"✅ Loaded custom palette with {len(custom_colors)} colors")
        
        # Display colors
        print("📋 Custom palette colors:")
        for i, color in enumerate(custom_colors):
            print(f"  {i+1:2}: {color}")
        
        return custom_colors
    except ImportError:
        print("❌ Custom palette not found, using default")
        return None

def test_ditherer_initialization(custom_colors):
    """Test ditherer initialization"""
    print("\n🔧 Testing Ditherer Initialization")
    print("=" * 40)
    
    # Test with custom colors
    ditherer = MinecraftDitherer(custom_colors)
    
    # Get palette info
    info = ditherer.get_palette_info()
    print(f"✅ Initialized ditherer")
    print(f"   Colors: {info['color_count']}")
    print(f"   Algorithm: {info['algorithm']}")
    print(f"   Color space: {info['color_space']}")
    
    return ditherer

def test_basic_dithering(ditherer):
    """Test basic dithering functionality"""
    print("\n🖼️  Testing Basic Dithering")
    print("=" * 40)
    
    # Create test images
    test_images = create_test_images()
    
    results = {}
    
    for name, image in test_images.items():
        print(f"\n🔄 Testing with {name} image ({image.size[0]}x{image.size[1]})")
        
        start_time = time.time()
        
        # Test dithering
        dithered = ditherer.dither_image(image, resize_for_minecraft=True)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"   ✅ Completed in {processing_time:.3f} seconds")
        print(f"   📏 Output size: {dithered.size}")
        
        results[name] = {
            'original': image,
            'dithered': dithered,
            'time': processing_time
        }
    
    return results

def test_comparison_mode(ditherer):
    """Test comparison mode (original, quantized, dithered)"""
    print("\n🔍 Testing Comparison Mode")
    print("=" * 40)
    
    # Create a test image
    test_image = create_test_images()['gradient']
    
    print("🔄 Generating comparison images...")
    original, quantized, dithered = ditherer.dither_with_comparison(test_image)
    
    print(f"✅ Generated comparison images:")
    print(f"   Original: {original.size}")
    print(f"   Quantized: {quantized.size}")
    print(f"   Dithered: {dithered.size}")
    
    return original, quantized, dithered

def test_palette_preview(ditherer):
    """Test palette preview generation"""
    print("\n🎨 Testing Palette Preview")
    print("=" * 40)
    
    success = ditherer.save_palette_preview("test_palette_preview.png")
    
    if success:
        print("✅ Palette preview generated successfully")
        return True
    else:
        print("❌ Failed to generate palette preview")
        return False

def test_progress_tracking(ditherer):
    """Test progress tracking functionality"""
    print("\n📊 Testing Progress Tracking")
    print("=" * 40)
    
    # Create a larger test image for visible progress
    large_image = Image.new('RGB', (100, 100))
    for y in range(100):
        for x in range(100):
            r = int((x / 99) * 255)
            g = int((y / 99) * 255)
            b = 128
            large_image.putpixel((x, y), (r, g, b))
    
    print("🔄 Testing progress callback with 100x100 image...")
    
    progress_updates = []
    
    def test_progress_callback(current, total):
        progress_updates.append((current, total))
        if len(progress_updates) % 1000 == 0 or current == total:
            percent = (current / total) * 100
            print(f"   Progress: {current}/{total} ({percent:.1f}%)")
    
    ditherer.set_progress_callback(test_progress_callback)
    
    # Dither with progress tracking
    dithered = ditherer.dither_image(large_image, resize_for_minecraft=False)
    
    print(f"✅ Progress tracking test complete")
    print(f"   Total progress updates: {len(progress_updates)}")
    print(f"   Final progress: {progress_updates[-1] if progress_updates else 'None'}")
    
    return len(progress_updates) > 0

def test_error_handling():
    """Test error handling"""
    print("\n⚠️  Testing Error Handling")
    print("=" * 40)
    
    # Test with invalid image
    try:
        ditherer = MinecraftDitherer()
        result = ditherer.dither_image(None)
        print("❌ Should have failed with None image")
        return False
    except Exception as e:
        print(f"✅ Correctly handled None image: {type(e).__name__}")
    
    # Test with empty color list
    try:
        ditherer = MinecraftDitherer([])
        print("❌ Should have failed with empty palette")
        return False
    except Exception as e:
        print(f"✅ Correctly handled empty palette: {type(e).__name__}")
    
    return True

def save_test_results(results):
    """Save test results for visual inspection"""
    print("\n💾 Saving Test Results")
    print("=" * 40)
    
    # Create output directory
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    saved_files = []
    
    for name, data in results.items():
        # Save original
        original_path = output_dir / f"{name}_original.png"
        data['original'].save(original_path)
        
        # Save dithered
        dithered_path = output_dir / f"{name}_dithered.png"
        data['dithered'].save(dithered_path)
        
        saved_files.extend([original_path, dithered_path])
        
        print(f"✅ Saved {name} test images")
    
    print(f"📁 All test images saved to: {output_dir}")
    return saved_files

def main():
    """Run all Phase 2 tests"""
    print("🚀 Minecraft Map Art Ditherer - Phase 2 Tests")
    print("=" * 50)
    
    try:
        # Test 1: Custom palette loading
        custom_colors = test_custom_palette_loading()
        
        # Test 2: Ditherer initialization
        ditherer = test_ditherer_initialization(custom_colors)
        
        # Test 3: Basic dithering
        results = test_basic_dithering(ditherer)
        
        # Test 4: Comparison mode
        comparison_results = test_comparison_mode(ditherer)
        
        # Test 5: Palette preview
        preview_success = test_palette_preview(ditherer)
        
        # Test 6: Progress tracking
        progress_success = test_progress_tracking(ditherer)
        
        # Test 7: Error handling
        error_handling_success = test_error_handling()
        
        # Save test results
        saved_files = save_test_results(results)
        
        # Summary
        print("\n📋 Test Summary")
        print("=" * 40)
        
        tests = [
            ("Custom Palette Loading", custom_colors is not None),
            ("Ditherer Initialization", True),
            ("Basic Dithering", len(results) > 0),
            ("Comparison Mode", comparison_results is not None),
            ("Palette Preview", preview_success),
            ("Progress Tracking", progress_success),
            ("Error Handling", error_handling_success)
        ]
        
        all_passed = True
        for test_name, passed in tests:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {test_name:25} {status}")
            if not passed:
                all_passed = False
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        if all_passed:
            print("\n🎉 Phase 2 dithering algorithm is working perfectly!")
            print("   Ready for Phase 3: GUI Development")
            print(f"   Test images saved: {len(saved_files)} files")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 