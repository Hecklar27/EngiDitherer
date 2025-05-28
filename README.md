# Minecraft Map Art Ditherer

A specialized dithering tool optimized for creating Minecraft Java Edition flat map art using carpet blocks.

## 🎯 Project Overview

This tool converts regular images into dithered versions that look great when built as Minecraft map art using carpet blocks. It uses a custom dithering algorithm specifically optimized for Minecraft's limited carpet color palette.

## ✨ Features

- **Minecraft-Optimized**: Uses exact carpet color palette from Java Edition
- **Intelligent Dithering**: Custom Floyd-Steinberg variant for limited palettes
- **Simple GUI**: Drag-and-drop interface for easy use
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

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Phase 1 Testing

Test the core infrastructure:

```bash
python test_phase1.py
```

This will test:
- Color palette loading (61 Minecraft carpet colors)
- Image processing utilities
- Color matching algorithms
- Integration between components

### Extract Colors from Your Palette (Optional)

If you have your own color palette file:

```bash
python extract_colors.py
```

Supported formats:
- `.act` (Adobe Color Table)
- `.png` (PNG with palette or unique colors)
- `.txt` (Text file with hex colors)

## 📁 Project Structure

```
minecraft-ditherer/
├── src/
│   ├── palette.py          # Minecraft color palette manager
│   ├── image_utils.py      # Image processing utilities
│   ├── dithering.py        # Dithering algorithm (Phase 2)
│   └── main.py            # GUI application (Phase 3)
├── memory-bank/           # Project documentation
├── test_phase1.py         # Phase 1 tests
├── extract_colors.py      # Color extraction utility
├── requirements.txt       # Python dependencies
└── README.md             # This file
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

## 🔧 Development Phases

### ✅ Phase 1: Core Infrastructure (Current)
- [x] Color palette manager with 61 Minecraft carpet colors
- [x] Image processing utilities
- [x] Color matching using LAB color space
- [x] Basic testing framework

### 🚧 Phase 2: Dithering Algorithm (Next)
- [ ] Custom Floyd-Steinberg implementation
- [ ] Error diffusion optimization for limited palettes
- [ ] Performance optimization
- [ ] Command-line interface

### 📋 Phase 3: GUI Development
- [ ] tkinter-based interface
- [ ] Drag-and-drop file loading
- [ ] Real-time preview
- [ ] Progress feedback

### 🎯 Phase 4: Optimization & Testing
- [ ] Performance improvements
- [ ] Comprehensive testing
- [ ] User experience refinements

### 📦 Phase 5: Distribution
- [ ] Standalone executable
- [ ] User documentation
- [ ] Distribution package

## 🧪 Testing

Run the Phase 1 tests to verify everything is working:

```bash
python test_phase1.py
```

Expected output:
```
🚀 Minecraft Map Art Ditherer - Phase 1 Tests
==================================================
🎨 Testing Color Palette Manager
========================================
✅ Loaded 61 Minecraft carpet colors

🔍 Color Matching Tests:
  Pure Red     (255, 0, 0) -> #DC0000 (distance: 32.1)
  Pure Green   (0, 255, 0) -> #00BB32 (distance: 45.2)
  ...

📋 Test Summary
========================================
  Color Palette Manager    ✅ PASSED
  Image Processing         ✅ PASSED
  Integration             ✅ PASSED

🎯 Overall Result: ✅ ALL TESTS PASSED

🎉 Phase 1 infrastructure is ready!
   Next: Implement the dithering algorithm (Phase 2)
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