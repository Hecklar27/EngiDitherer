# Minecraft Map Art Ditherer

A specialized dithering tool optimized for creating Minecraft Java Edition flat map art using carpet blocks.

## 🎯 Project Overview

This tool converts regular images into dithered versions that look great when built as Minecraft map art using carpet blocks. It uses a custom dithering algorithm specifically optimized for Minecraft's limited carpet color palette.

## ✨ Features

- **Minecraft-Optimized**: Uses exact carpet color palette from Java Edition
- **Multi-Map Support**: Create large map art using multiple maps (1×1 to 8×8 configurations)
- **Intelligent Dithering**: Custom Floyd-Steinberg variant for limited palettes
- **Simple GUI**: Drag-and-drop interface with map size selection
- **Fast Processing**: Optimized for quick iteration
- **Multiple Formats**: Supports PNG, JPG, BMP, TIFF, GIF

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd minecraft-ditherer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### 🎮 GUI Application (Recommended)

Launch the user-friendly graphical interface:

```bash
python launch_gui.py
```

**GUI Features:**
- Drag-and-drop image loading (or click to browse)
- Real-time preview with Original/Dithered tabs
- Progress bars and status updates
- Settings panel with Minecraft map resize option
- **Map size selection**: Choose from 1×1 to 8×8 map configurations
- Palette preview window
- Save functionality with file dialogs
- Comparison mode generation

#### 💻 Command Line Interface

For batch processing or advanced users:

```bash
# Basic dithering (single 128×128 map)
python dither_cli.py input.jpg

# Specify output file
python dither_cli.py input.png -o output.png

# Create 2×2 maps (256×256 pixels total)
python dither_cli.py input.jpg --map-width 2 --map-height 2

# Create wide format (1×2 maps, 128×256 pixels)
python dither_cli.py input.jpg --map-width 1 --map-height 2

# Generate comparison images
python dither_cli.py input.jpg --comparison

# Don't resize to Minecraft map size
python dither_cli.py input.jpg --no-resize

# Show palette preview
python dither_cli.py --palette-preview
```

#### 🗺️ Multi-Map Configurations

The tool supports creating large map art using multiple Minecraft maps arranged in grids:

| Configuration | Pixel Size | Total Maps | Use Case |
|---------------|------------|------------|----------|
| 1×1 maps | 128×128 | 1 | Standard single map |
| 2×1 maps | 256×128 | 2 | Wide format |
| 1×2 maps | 128×256 | 2 | Tall format |
| 2×2 maps | 256×256 | 4 | Large square |
| 3×3 maps | 384×384 | 9 | Extra large |
| 4×4 maps | 512×512 | 16 | Massive builds |
| Up to 8×8 | 1024×1024 | 64 | Maximum size |

**Examples:**
```bash
# Single map (default)
python dither_cli.py image.jpg

# Large 4×4 map wall
python dither_cli.py image.jpg --map-width 4 --map-height 4

# Wide banner (6×2 maps)
python dither_cli.py image.jpg --map-width 6 --map-height 2
```

#### 🧪 Testing

Test all components:

```bash
python test_phase3.py
```

Test the multi-map feature specifically:

```bash
python test_multimap.py
```

### Extract Colors from Your Palette (Optional)

If you have your own color palette file:

```bash
python extract_colors.py
```

Supported formats:
- `.act` (Adobe Color Table)
- `.png` (PNG with palette or unique colors)
- `.txt` (Text file with hex colors)

## 🎨 Demo Images

The project includes demo images for testing:

- `demo_images/gradient_demo.png` - Color gradient test pattern
- `demo_images/bands_demo.png` - Color band test pattern  
- `demo_images/checker_demo.png` - Checkerboard pattern

These are automatically created when running tests and are perfect for testing the dithering algorithm.

## 📁 Project Structure

```
minecraft-ditherer/
├── src/
│   ├── main.py           # GUI application ✅
│   ├── dithering.py      # Custom dithering algorithm ✅
│   ├── palette.py        # Color palette management ✅
│   └── image_utils.py    # Image processing utilities ✅
├── dither_cli.py         # Command-line interface ✅
├── launch_gui.py         # GUI launcher ✅
├── test_phase3.py        # Comprehensive testing ✅
├── extract_colors.py     # Color extraction utility ✅
├── requirements.txt      # Python dependencies ✅
├── minecraft_colors.py   # Custom 16-color palette ✅
├── demo_images/          # Test images ✅
└── memory-bank/          # Project documentation ✅
    ├── projectbrief.md
    ├── activeContext.md
    ├── progress.md
    └── ...
```

## 🎨 Color Palette

The tool uses 61 carefully selected carpet colors from Minecraft Java Edition that work for flat map art:

- Reds: `#DC0000`, `#A3292A`, `#842C2C`, `#8A4243`, `#7A3327`, `#600100`, `#4F1519`
- Oranges: `#BA6D2C`, `#A0721F`, `#89461F`, `#6F4A2A`, `#7B663E`, `#58412C`
- Yellows: `#D5C98C`, `#C5C52C`, `#D7CD42`
- Greens: `#6D9930`, `#6DB015`, `#58642D`, `#586D2C`, `#414624`, `#006A00`, `#00BB32`
- Blues: `#5884BA`, `#3F6EDC`, `#3737DC`, `#2C4199`, `#4FBCB7`
- Purples: `#9941BA`, `#6D3699`, `#8A8ADC`
- Grays: `#8D909E`, `#605D77`, `#DCDCDC`, `#DCD9D3`, `#ABABAB`, `#909090`, `#848484`, `#606060`, `#565656`, `#4B4F4F`, `#414141`, `#151515`
- And more...

## ✅ Project Status

**🎉 COMPLETE - All phases finished successfully!**

### ✅ Phase 1: Core Infrastructure 
- [x] Color palette manager with custom 16-color support
- [x] Image processing utilities with validation
- [x] Color matching using LAB color space for accuracy
- [x] Comprehensive testing framework

### ✅ Phase 2: Dithering Algorithm
- [x] Custom Floyd-Steinberg error diffusion implementation
- [x] Optimized for limited color palettes (16 colors)
- [x] Performance optimization (~2.5 seconds for 128x128)
- [x] Full-featured command-line interface

### ✅ Phase 3: GUI Application
- [x] Professional tkinter-based interface
- [x] Drag-and-drop file loading (click to browse)
- [x] Real-time preview with tabbed interface
- [x] Progress bars and multi-threaded processing
- [x] Settings panel and palette preview
- [x] Save/export functionality

**Ready for production use in Minecraft map art creation!**

## 🧪 Testing

Run the comprehensive tests to verify everything is working:

```bash
python test_phase3.py
```

Expected output:
```
🚀 Minecraft Map Art Ditherer - Phase 3 Tests
==================================================
🖥️  Testing GUI Imports
✅ tkinter imported successfully
✅ PIL/Pillow with tkinter support imported successfully
✅ Threading and queue modules imported successfully

🔗 Testing Ditherer Integration
✅ Custom palette loaded: 16 colors
✅ Ditherer initialized with 16 colors

🎮 Testing GUI Creation
✅ DithererGUI initialized successfully
✅ All GUI components initialized correctly

📋 Test Summary
========================================
  GUI Imports               ✅ PASSED
  Ditherer Integration      ✅ PASSED
  Image Processing          ✅ PASSED
  GUI Creation              ✅ PASSED
  Threading Functionality   ✅ PASSED
  File Operations           ✅ PASSED
  Error Handling            ✅ PASSED
  Demo Image Creation       ✅ PASSED

🎯 Overall Result: ✅ ALL TESTS PASSED

🎉 Phase 3 GUI application is ready!
🚀 Ready to launch GUI application!
```

## 🤝 Contributing

This project is in active development. Current focus is on Phase 1 completion and moving to Phase 2 (dithering algorithm implementation).

## 📄 License

[Add your license here]

## 🎮 Minecraft Compatibility

- **Edition**: Java Edition
- **Versions**: 1.17-1.20+
- **Map Type**: Flat maps (128x128 pixels)
- **Blocks**: Carpet blocks only (61 colors)

## 🔗 Useful Links

- [Minecraft Wiki - Map Item Format](https://minecraft.wiki/w/Map_item_format)
- [Minecraft Map Art Community](https://www.reddit.com/r/MinecraftMapArt/)
- [Color Theory for Dithering](https://en.wikipedia.org/wiki/Dither) 