"""
Custom Dithering Algorithm for Minecraft Map Art
Optimized Floyd-Steinberg implementation for limited color palettes
"""

import numpy as np
from PIL import Image
from typing import Tuple, List, Optional, Callable
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from palette import MinecraftPalette
from image_utils import ImageProcessor

class MinecraftDitherer:
    """
    Custom dithering algorithm optimized for Minecraft map art
    Uses Floyd-Steinberg error diffusion with palette-specific optimizations
    """
    
    def __init__(self, custom_colors: Optional[List[str]] = None):
        """
        Initialize the ditherer with color palette
        
        Args:
            custom_colors: Optional list of hex colors to use instead of default palette
        """
        self.palette = MinecraftPalette()
        
        # Use custom colors if provided
        if custom_colors:
            self.palette.CARPET_COLORS = custom_colors
            self.palette.__init__()  # Reinitialize with new colors
            print(f"✅ Loaded custom palette with {len(custom_colors)} colors")
        
        # Floyd-Steinberg error diffusion matrix
        # Distributes error to neighboring pixels:
        #     * 7/16
        # 3/16 5/16 1/16
        self.error_matrix = np.array([
            [0, 0, 7/16],
            [3/16, 5/16, 1/16]
        ])
        
        self.processed_pixels = 0
        self.total_pixels = 0
        self.progress_callback = None
    
    def set_progress_callback(self, callback: Callable[[int, int], None]):
        """Set a callback function for progress updates"""
        self.progress_callback = callback
    
    def _update_progress(self):
        """Update progress if callback is set"""
        if self.progress_callback:
            self.progress_callback(self.processed_pixels, self.total_pixels)
    
    def _find_closest_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, Tuple[int, int, int], np.ndarray]:
        """
        Find closest color in palette and return error
        
        Args:
            rgb: Target RGB color
            
        Returns:
            (index, closest_rgb, error_rgb)
        """
        idx, closest_rgb, _ = self.palette.find_closest_color(rgb, method="lab")
        
        # Calculate error for diffusion
        error = np.array(rgb, dtype=np.float64) - np.array(closest_rgb, dtype=np.float64)
        
        return idx, closest_rgb, error
    
    def _apply_error_diffusion(self, image_array: np.ndarray, x: int, y: int, error: np.ndarray):
        """
        Apply Floyd-Steinberg error diffusion to neighboring pixels
        
        Args:
            image_array: Image array being processed (modified in place)
            x, y: Current pixel coordinates
            error: RGB error to distribute
        """
        height, width = image_array.shape[:2]
        
        # Apply error to neighboring pixels according to Floyd-Steinberg matrix
        for dy in range(self.error_matrix.shape[0]):
            for dx in range(self.error_matrix.shape[1]):
                # Calculate neighbor coordinates
                nx = x + dx - 1  # -1 because matrix starts at previous column
                ny = y + dy + 1  # +1 because we're looking at next row
                
                # Check bounds
                if 0 <= nx < width and 0 <= ny < height:
                    # Get error weight
                    weight = self.error_matrix[dy, dx]
                    
                    if weight > 0:
                        # Apply weighted error to neighbor
                        weighted_error = error * weight
                        
                        # Add error to neighbor pixel (with clamping)
                        for c in range(3):  # RGB channels
                            new_value = image_array[ny, nx, c] + weighted_error[c]
                            image_array[ny, nx, c] = np.clip(new_value, 0, 255)
    
    def dither_image(self, image: Image.Image, resize_for_minecraft: bool = True) -> Image.Image:
        """
        Apply dithering to an image
        
        Args:
            image: Input PIL Image
            resize_for_minecraft: Whether to resize to 128x128 for Minecraft maps
            
        Returns:
            Dithered PIL Image
        """
        print("🎨 Starting dithering process...")
        
        # Prepare image
        if resize_for_minecraft:
            image = ImageProcessor.resize_for_minecraft(image)
            print(f"📏 Resized to Minecraft map size: {image.size}")
        
        # Convert to RGB array
        image_array = ImageProcessor.image_to_array(image).astype(np.float64)
        height, width = image_array.shape[:2]
        
        # Initialize progress tracking
        self.total_pixels = height * width
        self.processed_pixels = 0
        
        print(f"🔄 Processing {width}x{height} pixels ({self.total_pixels} total)")
        
        # Create output array
        output_array = np.zeros_like(image_array, dtype=np.uint8)
        
        # Process each pixel
        for y in range(height):
            for x in range(width):
                # Get current pixel color
                current_rgb = tuple(image_array[y, x].astype(int))
                
                # Find closest palette color and calculate error
                idx, closest_rgb, error = self._find_closest_color(current_rgb)
                
                # Set output pixel to closest color
                output_array[y, x] = closest_rgb
                
                # Apply error diffusion to neighboring pixels
                self._apply_error_diffusion(image_array, x, y, error)
                
                # Update progress
                self.processed_pixels += 1
                if self.processed_pixels % 1000 == 0:  # Update every 1000 pixels
                    self._update_progress()
        
        # Final progress update
        self._update_progress()
        
        # Convert back to PIL Image
        result_image = ImageProcessor.array_to_image(output_array)
        
        print("✅ Dithering complete!")
        return result_image
    
    def dither_with_comparison(self, image: Image.Image, resize_for_minecraft: bool = True) -> Tuple[Image.Image, Image.Image, Image.Image]:
        """
        Dither image and return original, quantized (no dithering), and dithered versions
        
        Args:
            image: Input PIL Image
            resize_for_minecraft: Whether to resize to 128x128
            
        Returns:
            (original_image, quantized_image, dithered_image)
        """
        # Prepare original
        if resize_for_minecraft:
            original = ImageProcessor.resize_for_minecraft(image)
        else:
            original = image.copy()
        
        # Create quantized version (no dithering)
        quantized = self._create_quantized_image(original)
        
        # Create dithered version
        dithered = self.dither_image(original, resize_for_minecraft=False)  # Already resized
        
        return original, quantized, dithered
    
    def _create_quantized_image(self, image: Image.Image) -> Image.Image:
        """Create a quantized version without dithering for comparison"""
        image_array = ImageProcessor.image_to_array(image)
        height, width = image_array.shape[:2]
        
        output_array = np.zeros_like(image_array, dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                current_rgb = tuple(image_array[y, x])
                _, closest_rgb, _ = self.palette.find_closest_color(current_rgb, method="lab")
                output_array[y, x] = closest_rgb
        
        return ImageProcessor.array_to_image(output_array)
    
    def get_palette_info(self) -> dict:
        """Get information about the current palette"""
        return {
            "color_count": len(self.palette.CARPET_COLORS),
            "colors": self.palette.CARPET_COLORS.copy(),
            "color_space": "LAB (perceptual)",
            "algorithm": "Floyd-Steinberg Error Diffusion"
        }
    
    def save_palette_preview(self, output_path: str, swatch_size: int = 50) -> bool:
        """
        Save a visual preview of the color palette
        
        Args:
            output_path: Path to save the preview image
            swatch_size: Size of each color swatch in pixels
            
        Returns:
            True if successful
        """
        try:
            colors = self.palette.CARPET_COLORS
            cols = 4  # 4 colors per row
            rows = (len(colors) + cols - 1) // cols  # Ceiling division
            
            # Create preview image
            preview_width = cols * swatch_size
            preview_height = rows * swatch_size
            preview = Image.new('RGB', (preview_width, preview_height), 'white')
            
            # Draw color swatches
            for i, hex_color in enumerate(colors):
                row = i // cols
                col = i % cols
                
                # Convert hex to RGB
                rgb = self.palette.hex_to_rgb(hex_color)
                
                # Create swatch
                x1 = col * swatch_size
                y1 = row * swatch_size
                x2 = x1 + swatch_size
                y2 = y1 + swatch_size
                
                # Fill swatch area
                for y in range(y1, y2):
                    for x in range(x1, x2):
                        if x < preview_width and y < preview_height:
                            preview.putpixel((x, y), rgb)
            
            # Save preview
            preview.save(output_path)
            print(f"✅ Saved palette preview: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving palette preview: {e}")
            return False

# Test function
def test_dithering():
    """Test the dithering functionality"""
    print("🧪 Testing Minecraft Dithering Algorithm")
    print("=" * 50)
    
    # Load custom colors if available
    try:
        sys.path.append('.')
        from minecraft_colors import MINECRAFT_CARPET_COLORS
        custom_colors = MINECRAFT_CARPET_COLORS
        print(f"📦 Using custom palette with {len(custom_colors)} colors")
    except ImportError:
        custom_colors = None
        print("📦 Using default palette")
    
    # Initialize ditherer
    ditherer = MinecraftDitherer(custom_colors)
    
    # Get palette info
    info = ditherer.get_palette_info()
    print(f"🎨 Palette: {info['color_count']} colors using {info['color_space']}")
    
    # Create test image
    test_image = Image.new('RGB', (64, 64))
    
    # Create a gradient test pattern
    for y in range(64):
        for x in range(64):
            r = int((x / 63) * 255)
            g = int((y / 63) * 255)
            b = 128
            test_image.putpixel((x, y), (r, g, b))
    
    print("🖼️  Created test gradient image (64x64)")
    
    # Test dithering
    print("🔄 Testing dithering process...")
    
    def progress_callback(current, total):
        if current % 2000 == 0 or current == total:
            percent = (current / total) * 100
            print(f"   Progress: {current}/{total} pixels ({percent:.1f}%)")
    
    ditherer.set_progress_callback(progress_callback)
    
    # Dither the image
    dithered = ditherer.dither_image(test_image)
    
    print(f"✅ Dithering complete! Output size: {dithered.size}")
    
    # Save palette preview
    ditherer.save_palette_preview("palette_preview.png")
    
    return True

if __name__ == "__main__":
    test_dithering() 