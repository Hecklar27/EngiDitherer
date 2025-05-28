"""
Minecraft Carpet Color Palette Manager
Handles color matching and distance calculations for map art dithering
"""

import numpy as np
from colorspacious import cspace_convert
from typing import List, Tuple, Dict
import colorsys

class MinecraftPalette:
    """Manages Minecraft carpet colors and provides color matching functionality"""
    
    # Minecraft Java Edition carpet colors for flat map art (61 colors)
    CARPET_COLORS = [
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
    
    def __init__(self):
        """Initialize the palette with precomputed color data"""
        if not self.CARPET_COLORS:
            raise ValueError("Color palette cannot be empty")
            
        self.colors_rgb = []
        self.colors_lab = []
        self.color_names = []
        
        # Convert hex colors to RGB and LAB
        for i, hex_color in enumerate(self.CARPET_COLORS):
            rgb = self.hex_to_rgb(hex_color)
            lab = self.rgb_to_lab(rgb)
            
            self.colors_rgb.append(rgb)
            self.colors_lab.append(lab)
            self.color_names.append(f"Carpet_{i+1}")
        
        # Convert to numpy arrays for efficient computation
        self.colors_rgb = np.array(self.colors_rgb)
        self.colors_lab = np.array(self.colors_lab)
        
        print(f"✅ Loaded {len(self.CARPET_COLORS)} Minecraft carpet colors")
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    
    @staticmethod
    def rgb_to_lab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to LAB color space for perceptual color matching"""
        # Normalize RGB to 0-1 range
        rgb_normalized = [c / 255.0 for c in rgb]
        # Convert to LAB using colorspacious
        lab = cspace_convert(rgb_normalized, "sRGB1", "CIELab")
        return tuple(lab)
    
    def find_closest_color_rgb(self, target_rgb: Tuple[int, int, int]) -> Tuple[int, Tuple[int, int, int], str]:
        """
        Find closest carpet color using RGB distance
        Returns: (index, rgb_color, hex_color)
        """
        target = np.array(target_rgb)
        distances = np.sqrt(np.sum((self.colors_rgb - target) ** 2, axis=1))
        closest_idx = np.argmin(distances)
        
        closest_rgb = tuple(self.colors_rgb[closest_idx])
        closest_hex = self.CARPET_COLORS[closest_idx]
        
        return closest_idx, closest_rgb, closest_hex
    
    def find_closest_color_lab(self, target_rgb: Tuple[int, int, int]) -> Tuple[int, Tuple[int, int, int], str]:
        """
        Find closest carpet color using LAB distance (perceptually accurate)
        Returns: (index, rgb_color, hex_color)
        """
        target_lab = np.array(self.rgb_to_lab(target_rgb))
        distances = np.sqrt(np.sum((self.colors_lab - target_lab) ** 2, axis=1))
        closest_idx = np.argmin(distances)
        
        closest_rgb = tuple(self.colors_rgb[closest_idx])
        closest_hex = self.CARPET_COLORS[closest_idx]
        
        return closest_idx, closest_rgb, closest_hex
    
    def find_closest_color(self, target_rgb: Tuple[int, int, int], method: str = "lab") -> Tuple[int, Tuple[int, int, int], str]:
        """
        Find closest carpet color using specified method
        
        Args:
            target_rgb: Target color as (R, G, B) tuple
            method: "lab" for perceptual matching, "rgb" for simple RGB distance
            
        Returns:
            (index, rgb_color, hex_color)
        """
        if method.lower() == "lab":
            return self.find_closest_color_lab(target_rgb)
        else:
            return self.find_closest_color_rgb(target_rgb)
    
    def get_color_info(self, index: int) -> Dict:
        """Get detailed information about a color by index"""
        if 0 <= index < len(self.CARPET_COLORS):
            return {
                "index": index,
                "hex": self.CARPET_COLORS[index],
                "rgb": tuple(self.colors_rgb[index]),
                "lab": tuple(self.colors_lab[index]),
                "name": self.color_names[index]
            }
        return None
    
    def get_palette_preview(self) -> List[str]:
        """Get a list of all colors for preview purposes"""
        return self.CARPET_COLORS.copy()
    
    def calculate_color_distance(self, color1_rgb: Tuple[int, int, int], 
                                color2_rgb: Tuple[int, int, int], 
                                method: str = "lab") -> float:
        """Calculate distance between two colors"""
        if method.lower() == "lab":
            lab1 = np.array(self.rgb_to_lab(color1_rgb))
            lab2 = np.array(self.rgb_to_lab(color2_rgb))
            return np.sqrt(np.sum((lab1 - lab2) ** 2))
        else:
            rgb1 = np.array(color1_rgb)
            rgb2 = np.array(color2_rgb)
            return np.sqrt(np.sum((rgb1 - rgb2) ** 2))

# Test function
def test_palette():
    """Test the palette functionality"""
    print("Testing Minecraft Palette...")
    palette = MinecraftPalette()
    
    # Test color matching
    test_colors = [
        (255, 0, 0),    # Pure red
        (0, 255, 0),    # Pure green
        (0, 0, 255),    # Pure blue
        (128, 128, 128), # Gray
        (255, 255, 255), # White
        (0, 0, 0)       # Black
    ]
    
    print("\nColor matching tests:")
    for rgb in test_colors:
        idx, closest_rgb, closest_hex = palette.find_closest_color(rgb)
        distance = palette.calculate_color_distance(rgb, closest_rgb)
        print(f"Input: {rgb} -> Closest: {closest_hex} {closest_rgb} (distance: {distance:.2f})")

if __name__ == "__main__":
    test_palette() 