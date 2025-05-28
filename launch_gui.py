#!/usr/bin/env python3
"""
Minecraft Map Art Ditherer - GUI Launcher
Simple launcher for the GUI application
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the GUI application"""
    print("🎮 Launching Minecraft Map Art Ditherer GUI...")
    
    # Add src directory to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # Import and run the GUI
        from main import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 