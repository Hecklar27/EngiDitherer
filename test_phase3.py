#!/usr/bin/env python3
"""
Phase 3 Test Script for Minecraft Map Art Ditherer
Tests the GUI application functionality and integration
"""

import sys
import os
import time
import threading
from pathlib import Path

# Add src directory to path
sys.path.append('src')

def test_gui_imports():
    """Test that all GUI dependencies can be imported"""
    print("🖥️  Testing GUI Imports")
    print("=" * 40)
    
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        from tkinter import ttk, filedialog, messagebox
        print("✅ tkinter submodules imported successfully")
        
        from PIL import Image, ImageTk
        print("✅ PIL/Pillow with tkinter support imported successfully")
        
        import threading
        import queue
        print("✅ Threading and queue modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_ditherer_integration():
    """Test integration with dithering components"""
    print("\n🔗 Testing Ditherer Integration")
    print("=" * 40)
    
    try:
        from main import DithererGUI
        from dithering import MinecraftDitherer
        from image_utils import ImageProcessor
        
        print("✅ All main components imported successfully")
        
        # Test custom palette loading
        try:
            from minecraft_colors import MINECRAFT_CARPET_COLORS
            custom_colors = MINECRAFT_CARPET_COLORS
            print(f"✅ Custom palette loaded: {len(custom_colors)} colors")
        except ImportError:
            custom_colors = None
            print("⚠️  Custom palette not found, will use default")
        
        # Test ditherer initialization
        ditherer = MinecraftDitherer(custom_colors)
        info = ditherer.get_palette_info()
        print(f"✅ Ditherer initialized with {info['color_count']} colors")
        
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_image_processing():
    """Test image processing functionality"""
    print("\n🖼️  Testing Image Processing")
    print("=" * 40)
    
    try:
        from PIL import Image
        from image_utils import ImageProcessor
        
        # Create test image
        test_image = Image.new('RGB', (100, 100), (128, 128, 128))
        print("✅ Test image created")
        
        # Test image info
        info = ImageProcessor.get_image_info(test_image)
        print(f"✅ Image info: {info['width']}x{info['height']}, {info['mode']}")
        
        # Test validation
        is_valid, message = ImageProcessor.validate_image_for_processing(test_image)
        print(f"✅ Image validation: {message}")
        
        # Test thumbnail creation
        thumbnail = ImageProcessor.create_thumbnail(test_image, (50, 50))
        print(f"✅ Thumbnail created: {thumbnail.size}")
        
        return True
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

def test_gui_creation():
    """Test GUI creation without showing window"""
    print("\n🎮 Testing GUI Creation")
    print("=" * 40)
    
    try:
        import tkinter as tk
        from main import DithererGUI
        
        # Create root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        print("✅ Tkinter root window created")
        
        # Initialize GUI
        app = DithererGUI(root)
        print("✅ DithererGUI initialized successfully")
        
        # Test that key components exist
        assert hasattr(app, 'ditherer'), "Ditherer not initialized"
        assert hasattr(app, 'current_image'), "Current image variable not set"
        assert hasattr(app, 'progress_queue'), "Progress queue not created"
        assert hasattr(app, 'result_queue'), "Result queue not created"
        
        print("✅ All GUI components initialized correctly")
        
        # Test palette info
        if app.custom_colors:
            print(f"✅ Custom palette loaded: {len(app.custom_colors)} colors")
        else:
            print("✅ Default palette loaded")
        
        # Clean up
        root.destroy()
        print("✅ GUI cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ GUI creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_threading_functionality():
    """Test threading functionality for background processing"""
    print("\n🧵 Testing Threading Functionality")
    print("=" * 40)
    
    try:
        import threading
        import queue
        import time
        
        # Test queue communication
        test_queue = queue.Queue()
        result_queue = queue.Queue()
        
        def worker_function():
            """Test worker function"""
            for i in range(5):
                test_queue.put(i * 20)  # Progress updates
                time.sleep(0.1)
            result_queue.put("Worker completed successfully")
        
        # Start worker thread
        worker_thread = threading.Thread(target=worker_function)
        worker_thread.daemon = True
        worker_thread.start()
        
        print("✅ Worker thread started")
        
        # Monitor progress
        progress_updates = []
        while worker_thread.is_alive() or not test_queue.empty():
            try:
                progress = test_queue.get_nowait()
                progress_updates.append(progress)
                print(f"   Progress update: {progress}%")
            except queue.Empty:
                time.sleep(0.05)
        
        # Check result
        try:
            result = result_queue.get_nowait()
            print(f"✅ Worker result: {result}")
        except queue.Empty:
            print("❌ No result from worker")
            return False
        
        print(f"✅ Threading test complete: {len(progress_updates)} progress updates")
        return True
        
    except Exception as e:
        print(f"❌ Threading test failed: {e}")
        return False

def test_file_operations():
    """Test file operations and path handling"""
    print("\n📁 Testing File Operations")
    print("=" * 40)
    
    try:
        from pathlib import Path
        from image_utils import ImageProcessor
        from PIL import Image
        
        # Test supported formats
        test_files = ['test.png', 'test.jpg', 'test.bmp', 'test.gif']
        for file in test_files:
            supported = ImageProcessor.is_supported_format(file)
            status = "✅ Supported" if supported else "❌ Not supported"
            print(f"   {file}: {status}")
        
        # Test path operations
        test_path = Path("test_image.png")
        print(f"✅ Path operations: {test_path.stem}, {test_path.suffix}")
        
        # Test image creation and saving
        test_image = Image.new('RGB', (64, 64), (255, 0, 0))
        test_image.save("temp_test_image.png")
        print("✅ Test image saved")
        
        # Test image loading
        loaded_image = Image.open("temp_test_image.png")
        print(f"✅ Test image loaded: {loaded_image.size}")
        
        # Clean up (close image first on Windows)
        loaded_image.close()
        os.remove("temp_test_image.png")
        print("✅ Cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_error_handling():
    """Test error handling scenarios"""
    print("\n⚠️  Testing Error Handling")
    print("=" * 40)
    
    try:
        from image_utils import ImageProcessor
        
        # Test invalid file format
        supported = ImageProcessor.is_supported_format("test.xyz")
        assert not supported, "Should not support .xyz files"
        print("✅ Invalid format correctly rejected")
        
        # Test image validation with None
        is_valid, message = ImageProcessor.validate_image_for_processing(None)
        assert not is_valid, "Should reject None image"
        print("✅ None image correctly rejected")
        
        # Test non-existent file
        image = ImageProcessor.load_image("nonexistent_file.png")
        assert image is None, "Should return None for non-existent file"
        print("✅ Non-existent file correctly handled")
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def create_demo_images():
    """Create demo images for testing"""
    print("\n🎨 Creating Demo Images")
    print("=" * 40)
    
    try:
        from PIL import Image
        
        demo_dir = Path("demo_images")
        demo_dir.mkdir(exist_ok=True)
        
        # Create gradient image
        gradient = Image.new('RGB', (128, 128))
        for y in range(128):
            for x in range(128):
                r = int((x / 127) * 255)
                g = int((y / 127) * 255)
                b = 128
                gradient.putpixel((x, y), (r, g, b))
        
        gradient_path = demo_dir / "gradient_demo.png"
        gradient.save(gradient_path)
        print(f"✅ Created gradient demo: {gradient_path}")
        
        # Create color bands image
        bands = Image.new('RGB', (128, 128))
        for y in range(128):
            for x in range(128):
                if x < 32:
                    color = (255, 0, 0)  # Red
                elif x < 64:
                    color = (0, 255, 0)  # Green
                elif x < 96:
                    color = (0, 0, 255)  # Blue
                else:
                    color = (255, 255, 255)  # White
                bands.putpixel((x, y), color)
        
        bands_path = demo_dir / "bands_demo.png"
        bands.save(bands_path)
        print(f"✅ Created color bands demo: {bands_path}")
        
        # Create checkerboard image
        checker = Image.new('RGB', (128, 128))
        for y in range(128):
            for x in range(128):
                if (x // 16 + y // 16) % 2 == 0:
                    color = (0, 0, 0)  # Black
                else:
                    color = (255, 255, 255)  # White
                checker.putpixel((x, y), color)
        
        checker_path = demo_dir / "checker_demo.png"
        checker.save(checker_path)
        print(f"✅ Created checkerboard demo: {checker_path}")
        
        print(f"📁 Demo images saved to: {demo_dir}")
        return [gradient_path, bands_path, checker_path]
        
    except Exception as e:
        print(f"❌ Demo image creation failed: {e}")
        return []

def main():
    """Run all Phase 3 tests"""
    print("🚀 Minecraft Map Art Ditherer - Phase 3 Tests")
    print("=" * 50)
    
    try:
        # Test 1: GUI imports
        imports_success = test_gui_imports()
        
        # Test 2: Ditherer integration
        integration_success = test_ditherer_integration()
        
        # Test 3: Image processing
        image_success = test_image_processing()
        
        # Test 4: GUI creation
        gui_success = test_gui_creation()
        
        # Test 5: Threading functionality
        threading_success = test_threading_functionality()
        
        # Test 6: File operations
        file_success = test_file_operations()
        
        # Test 7: Error handling
        error_success = test_error_handling()
        
        # Test 8: Create demo images
        demo_images = create_demo_images()
        demo_success = len(demo_images) > 0
        
        # Summary
        print("\n📋 Test Summary")
        print("=" * 40)
        
        tests = [
            ("GUI Imports", imports_success),
            ("Ditherer Integration", integration_success),
            ("Image Processing", image_success),
            ("GUI Creation", gui_success),
            ("Threading Functionality", threading_success),
            ("File Operations", file_success),
            ("Error Handling", error_success),
            ("Demo Image Creation", demo_success)
        ]
        
        all_passed = True
        for test_name, passed in tests:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {test_name:25} {status}")
            if not passed:
                all_passed = False
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        if all_passed:
            print("\n🎉 Phase 3 GUI application is ready!")
            print("   All components tested and working correctly")
            print(f"   Demo images created: {len(demo_images)} files")
            print("\n🚀 Ready to launch GUI application!")
            print("   Run: python src/main.py")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 