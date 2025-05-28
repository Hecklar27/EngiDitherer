"""
Image Processing Utilities for Minecraft Map Art Ditherer
Handles image loading, validation, resizing, and format conversions
"""

from PIL import Image, ImageTk
import numpy as np
from typing import Tuple, Optional, List
import os

class ImageProcessor:
    """Handles image processing operations for the ditherer"""
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
    MAX_SIZE = (2048, 2048)  # Maximum image size for processing
    MINECRAFT_MAP_SIZE = (128, 128)  # Standard Minecraft map size
    
    def __init__(self):
        """Initialize the image processor"""
        pass
    
    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """Check if the file format is supported"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in ImageProcessor.SUPPORTED_FORMATS
    
    @staticmethod
    def load_image(file_path: str) -> Optional[Image.Image]:
        """
        Load an image from file with validation
        
        Args:
            file_path: Path to the image file
            
        Returns:
            PIL Image object or None if loading failed
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not ImageProcessor.is_supported_format(file_path):
                raise ValueError(f"Unsupported file format: {file_path}")
            
            # Load and convert to RGB
            image = Image.open(file_path)
            
            # Convert to RGB if necessary (handles RGBA, P, L modes)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Check image size
            if image.size[0] > ImageProcessor.MAX_SIZE[0] or image.size[1] > ImageProcessor.MAX_SIZE[1]:
                print(f"⚠️  Image is large ({image.size}), consider resizing for better performance")
            
            print(f"✅ Loaded image: {image.size[0]}x{image.size[1]} pixels")
            return image
            
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return None
    
    @staticmethod
    def resize_image(image: Image.Image, target_size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image to target size
        
        Args:
            image: PIL Image object
            target_size: Target (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized PIL Image object
        """
        if maintain_aspect:
            # Calculate size maintaining aspect ratio
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            return image
        else:
            # Resize to exact dimensions
            return image.resize(target_size, Image.Resampling.LANCZOS)
    
    @staticmethod
    def resize_for_minecraft(image: Image.Image, map_size: Tuple[int, int] = None) -> Image.Image:
        """
        Resize image for Minecraft map art
        
        Args:
            image: PIL Image object
            map_size: Target map size (default: 128x128)
            
        Returns:
            Resized image suitable for Minecraft maps
        """
        if map_size is None:
            map_size = ImageProcessor.MINECRAFT_MAP_SIZE
        
        # Resize maintaining aspect ratio, then crop/pad to exact size
        image_copy = image.copy()
        image_copy.thumbnail(map_size, Image.Resampling.LANCZOS)
        
        # Create new image with exact size and paste resized image centered
        final_image = Image.new('RGB', map_size, (0, 0, 0))
        
        # Calculate position to center the image
        x = (map_size[0] - image_copy.size[0]) // 2
        y = (map_size[1] - image_copy.size[1]) // 2
        
        final_image.paste(image_copy, (x, y))
        
        return final_image
    
    @staticmethod
    def image_to_array(image: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to numpy array
        
        Args:
            image: PIL Image object
            
        Returns:
            Numpy array with shape (height, width, 3) for RGB
        """
        return np.array(image)
    
    @staticmethod
    def array_to_image(array: np.ndarray) -> Image.Image:
        """
        Convert numpy array to PIL Image
        
        Args:
            array: Numpy array with shape (height, width, 3)
            
        Returns:
            PIL Image object
        """
        # Ensure array is in correct format
        array = np.clip(array, 0, 255).astype(np.uint8)
        return Image.fromarray(array, 'RGB')
    
    @staticmethod
    def save_image(image: Image.Image, output_path: str, quality: int = 95) -> bool:
        """
        Save image to file
        
        Args:
            image: PIL Image object
            output_path: Output file path
            quality: JPEG quality (if saving as JPEG)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Determine format from extension
            _, ext = os.path.splitext(output_path.lower())
            
            if ext in {'.jpg', '.jpeg'}:
                image.save(output_path, 'JPEG', quality=quality)
            elif ext == '.png':
                image.save(output_path, 'PNG')
            else:
                image.save(output_path)
            
            print(f"✅ Saved image: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving image: {e}")
            return False
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (200, 200)) -> Image.Image:
        """
        Create a thumbnail for preview purposes
        
        Args:
            image: PIL Image object
            size: Thumbnail size
            
        Returns:
            Thumbnail image
        """
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
    
    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        """
        Get detailed information about an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with image information
        """
        return {
            'size': image.size,
            'mode': image.mode,
            'format': getattr(image, 'format', 'Unknown'),
            'width': image.size[0],
            'height': image.size[1],
            'total_pixels': image.size[0] * image.size[1]
        }
    
    @staticmethod
    def validate_image_for_processing(image: Image.Image) -> Tuple[bool, str]:
        """
        Validate if image is suitable for processing
        
        Args:
            image: PIL Image object
            
        Returns:
            (is_valid, message)
        """
        if image is None:
            return False, "Image is None"
        
        if image.size[0] == 0 or image.size[1] == 0:
            return False, "Image has zero dimensions"
        
        if image.mode not in ['RGB', 'RGBA', 'L', 'P']:
            return False, f"Unsupported image mode: {image.mode}"
        
        total_pixels = image.size[0] * image.size[1]
        if total_pixels > 4194304:  # 2048x2048
            return False, "Image is too large (max 2048x2048)"
        
        return True, "Image is valid for processing"

# Test function
def test_image_utils():
    """Test the image utilities"""
    print("Testing Image Utilities...")
    
    # Test supported formats
    test_files = ['test.png', 'test.jpg', 'test.bmp', 'test.xyz']
    for file in test_files:
        supported = ImageProcessor.is_supported_format(file)
        print(f"Format {file}: {'✅ Supported' if supported else '❌ Not supported'}")
    
    # Create a test image
    test_image = Image.new('RGB', (256, 256), (128, 128, 128))
    
    # Test image info
    info = ImageProcessor.get_image_info(test_image)
    print(f"\nTest image info: {info}")
    
    # Test validation
    is_valid, message = ImageProcessor.validate_image_for_processing(test_image)
    print(f"Validation: {'✅' if is_valid else '❌'} {message}")
    
    # Test resizing
    resized = ImageProcessor.resize_for_minecraft(test_image)
    print(f"Resized for Minecraft: {resized.size}")

if __name__ == "__main__":
    test_image_utils() 