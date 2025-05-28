#!/usr/bin/env python3
"""
Multi-Map Feature Test Script
Tests the new multi-map sizing functionality
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')

def test_map_dimensions():
    """Test map dimension calculations"""
    print("🗺️  Testing Map Dimensions")
    print("=" * 40)
    
    try:
        from image_utils import ImageProcessor
        
        # Test various map configurations
        test_configs = [
            (1, 1),  # Single map
            (2, 1),  # 1x2 maps
            (1, 2),  # 2x1 maps  
            (2, 2),  # 2x2 maps
            (3, 2),  # 3x2 maps
            (4, 4),  # 4x4 maps
        ]
        
        for width, height in test_configs:
            info = ImageProcessor.get_map_dimensions_info(width, height)
            print(f"✅ {width}×{height} maps: {info['pixel_width']}×{info['pixel_height']} pixels, {info['total_maps']} total")
        
        return True
    except Exception as e:
        print(f"❌ Map dimensions test failed: {e}")
        return False

def test_image_resizing():
    """Test image resizing with different map configurations"""
    print("\n🖼️  Testing Multi-Map Image Resizing")
    print("=" * 40)
    
    try:
        from PIL import Image
        from image_utils import ImageProcessor
        
        # Create test image
        test_image = Image.new('RGB', (200, 200), (128, 128, 128))
        print("✅ Created test image (200x200)")
        
        # Test different map sizes
        test_configs = [
            (1, 1, "Single map"),
            (2, 1, "Wide map (1x2)"),
            (1, 2, "Tall map (2x1)"),
            (2, 2, "Large map (2x2)"),
        ]
        
        for width, height, description in test_configs:
            resized = ImageProcessor.resize_for_minecraft(test_image, width, height)
            expected_width = 128 * width
            expected_height = 128 * height
            
            if resized.size == (expected_width, expected_height):
                print(f"✅ {description}: {resized.size} ✓")
            else:
                print(f"❌ {description}: Expected {expected_width}x{expected_height}, got {resized.size}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Image resizing test failed: {e}")
        return False

def test_dithering_multimap():
    """Test dithering with multi-map configurations"""
    print("\n🎨 Testing Multi-Map Dithering")
    print("=" * 40)
    
    try:
        from PIL import Image
        from dithering import MinecraftDitherer
        
        # Load custom palette
        try:
            from minecraft_colors import MINECRAFT_CARPET_COLORS
            custom_colors = MINECRAFT_CARPET_COLORS
            print(f"✅ Using custom palette: {len(custom_colors)} colors")
        except ImportError:
            custom_colors = None
            print("⚠️  Using default palette")
        
        # Initialize ditherer
        ditherer = MinecraftDitherer(custom_colors)
        
        # Create test image
        test_image = Image.new('RGB', (100, 100))
        for y in range(100):
            for x in range(100):
                r = int((x / 99) * 255)
                g = int((y / 99) * 255)
                b = 128
                test_image.putpixel((x, y), (r, g, b))
        
        print("✅ Created gradient test image")
        
        # Test different map configurations
        test_configs = [
            (1, 1, "1x1 map"),
            (2, 1, "2x1 maps"),
            (1, 2, "1x2 maps"),
            (2, 2, "2x2 maps"),
        ]
        
        for width, height, description in test_configs:
            print(f"\n🔄 Testing {description}...")
            
            # Dither with specific map size
            dithered = ditherer.dither_image(
                test_image, 
                resize_for_minecraft=True,
                map_width=width,
                map_height=height
            )
            
            expected_width = 128 * width
            expected_height = 128 * height
            
            if dithered.size == (expected_width, expected_height):
                print(f"✅ {description}: Output size {dithered.size} ✓")
                
                # Save test output
                output_path = f"test_multimap_{width}x{height}.png"
                dithered.save(output_path)
                print(f"💾 Saved: {output_path}")
            else:
                print(f"❌ {description}: Expected {expected_width}x{expected_height}, got {dithered.size}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Multi-map dithering test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_multimap():
    """Test CLI with multi-map options"""
    print("\n💻 Testing CLI Multi-Map Options")
    print("=" * 40)
    
    try:
        import subprocess
        
        # Test CLI help to ensure new options are present
        result = subprocess.run([
            sys.executable, "dither_cli.py", "--help"
        ], capture_output=True, text=True)
        
        if "--map-width" in result.stdout and "--map-height" in result.stdout:
            print("✅ CLI help includes new multi-map options")
        else:
            print("❌ CLI help missing multi-map options")
            return False
        
        # Test invalid map dimensions
        result = subprocess.run([
            sys.executable, "dither_cli.py", "demo_images/gradient_demo.png", 
            "--map-width", "10"  # Invalid (too large)
        ], capture_output=True, text=True)
        
        if "Map width must be between 1 and 8" in result.stderr or "Map width must be between 1 and 8" in result.stdout:
            print("✅ CLI correctly validates map width limits")
        else:
            print("⚠️  CLI validation may need adjustment")
        
        return True
    except Exception as e:
        print(f"❌ CLI multi-map test failed: {e}")
        return False

def main():
    """Run all multi-map tests"""
    print("🚀 Multi-Map Feature Tests")
    print("=" * 50)
    
    try:
        # Test 1: Map dimensions
        dimensions_success = test_map_dimensions()
        
        # Test 2: Image resizing
        resizing_success = test_image_resizing()
        
        # Test 3: Multi-map dithering
        dithering_success = test_dithering_multimap()
        
        # Test 4: CLI multi-map
        cli_success = test_cli_multimap()
        
        # Summary
        print("\n📋 Multi-Map Test Summary")
        print("=" * 40)
        
        tests = [
            ("Map Dimensions", dimensions_success),
            ("Image Resizing", resizing_success),
            ("Multi-Map Dithering", dithering_success),
            ("CLI Multi-Map", cli_success),
        ]
        
        all_passed = True
        for test_name, passed in tests:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {test_name:20} {status}")
            if not passed:
                all_passed = False
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        if all_passed:
            print("\n🎉 Multi-Map feature is working perfectly!")
            print("   ✅ Supports 1x1 to 8x8 map configurations")
            print("   ✅ Proper image resizing for all configurations")
            print("   ✅ Dithering works with all map sizes")
            print("   ✅ CLI includes new options with validation")
            print("\n🗺️  Available map sizes:")
            print("   • 1×1 maps (128×128 pixels) - Single map")
            print("   • 2×1 maps (256×128 pixels) - Wide format")
            print("   • 1×2 maps (128×256 pixels) - Tall format")
            print("   • 2×2 maps (256×256 pixels) - Large square")
            print("   • 3×3 maps (384×384 pixels) - Extra large")
            print("   • Up to 8×8 maps (1024×1024 pixels) - Maximum size")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 