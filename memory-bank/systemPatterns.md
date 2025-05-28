# System Patterns - Minecraft Map Art Ditherer

## Architecture Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Processing      │    │  Color Palette  │
│                 │    │  Engine          │    │  Manager        │
│ - File Dialog   │◄──►│                  │◄──►│                 │
│ - Image Preview │    │ - Custom Dither  │    │ - Carpet Colors │
│ - Controls      │    │ - Color Mapping  │    │ - Distance Calc │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Core Components

### 1. GUI Application (main.py)
- **Pattern**: Model-View-Controller (MVC)
- **Responsibilities**: 
  - File selection and loading
  - Image display and preview
  - User controls and settings
  - Progress feedback

### 2. Dithering Engine (dithering.py)
- **Pattern**: Strategy Pattern for different algorithms
- **Responsibilities**:
  - Custom Minecraft-optimized dithering algorithm
  - Error diffusion calculations
  - Pixel-by-pixel processing

### 3. Color Palette Manager (palette.py)
- **Pattern**: Singleton for color data
- **Responsibilities**:
  - Load Minecraft carpet color definitions
  - Color distance calculations (Delta E or RGB distance)
  - Nearest color matching

### 4. Image Processor (image_utils.py)
- **Pattern**: Utility functions
- **Responsibilities**:
  - Image loading and validation
  - Format conversions
  - Resizing and preprocessing

## Key Design Decisions

### Custom Dithering Algorithm
- **Base**: Modified Floyd-Steinberg error diffusion
- **Optimization**: Weighted error distribution considering Minecraft's limited palette
- **Enhancement**: Perceptual color distance instead of simple RGB distance

### Color Matching Strategy
- Use LAB color space for perceptually accurate color matching
- Pre-calculate distance matrix for performance
- Consider visual impact of carpet block patterns

### Performance Considerations
- Process images in chunks for large files
- Use NumPy arrays for efficient pixel operations
- Implement progress callbacks for GUI feedback 