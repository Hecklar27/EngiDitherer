#!/usr/bin/env python3
"""
Minecraft Map Art Ditherer - GUI Application
Main tkinter-based interface for the dithering tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkFont
from PIL import Image, ImageTk
import threading
import queue
import sys
import os
from pathlib import Path
import time

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dithering import MinecraftDitherer
from image_utils import ImageProcessor

class DithererGUI:
    """Main GUI application for Minecraft Map Art Ditherer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Map Art Ditherer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.setup_styles()
        
        # Initialize variables
        self.current_image = None
        self.dithered_image = None
        self.original_preview = None
        self.dithered_preview = None
        self.ditherer = None
        self.processing = False
        
        # Queue for thread communication
        self.progress_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Load custom palette
        self.load_custom_palette()
        
        # Create GUI elements
        self.create_widgets()
        self.setup_drag_drop()
        
        # Start progress monitoring
        self.monitor_progress()
        
        print("🎮 Minecraft Map Art Ditherer GUI Started")
    
    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Preview.TLabel', relief='sunken', borderwidth=2)
        
    def load_custom_palette(self):
        """Load custom palette if available"""
        try:
            # Try to import from parent directory
            sys.path.append('..')
            from minecraft_colors import MINECRAFT_CARPET_COLORS
            self.custom_colors = MINECRAFT_CARPET_COLORS
            self.palette_info = f"Custom palette: {len(self.custom_colors)} colors"
        except ImportError:
            self.custom_colors = None
            self.palette_info = "Default palette: 61 colors"
        
        # Initialize ditherer
        self.ditherer = MinecraftDitherer(self.custom_colors)
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎮 Minecraft Map Art Ditherer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Center panel - Image preview
        self.create_preview_panel(main_frame)
        
        # Right panel - Settings and info
        self.create_info_panel(main_frame)
        
        # Bottom panel - Progress and status
        self.create_status_panel(main_frame)
    
    def create_control_panel(self, parent):
        """Create the left control panel"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Load image button
        self.load_btn = ttk.Button(control_frame, text="📁 Load Image", 
                                  command=self.load_image, style='Action.TButton')
        self.load_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Dither button
        self.dither_btn = ttk.Button(control_frame, text="🎨 Dither Image", 
                                    command=self.start_dithering, style='Action.TButton',
                                    state='disabled')
        self.dither_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Save button
        self.save_btn = ttk.Button(control_frame, text="💾 Save Result", 
                                  command=self.save_image, style='Action.TButton',
                                  state='disabled')
        self.save_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, 
                                                              sticky=(tk.W, tk.E), pady=10)
        
        # Comparison button
        self.comparison_btn = ttk.Button(control_frame, text="🔍 Generate Comparison", 
                                        command=self.generate_comparison,
                                        state='disabled')
        self.comparison_btn.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Palette preview button
        self.palette_btn = ttk.Button(control_frame, text="🎨 Show Palette", 
                                     command=self.show_palette_preview)
        self.palette_btn.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Configure column weight
        control_frame.columnconfigure(0, weight=1)
    
    def create_preview_panel(self, parent):
        """Create the center image preview panel"""
        preview_frame = ttk.LabelFrame(parent, text="Image Preview", padding="10")
        preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(preview_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Original image tab
        self.original_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.original_frame, text="Original")
        
        self.original_label = ttk.Label(self.original_frame, text="Drop an image here or click 'Load Image'",
                                       style='Preview.TLabel', anchor='center')
        self.original_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Dithered image tab
        self.dithered_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dithered_frame, text="Dithered")
        
        self.dithered_label = ttk.Label(self.dithered_frame, text="Dithered image will appear here",
                                       style='Preview.TLabel', anchor='center')
        self.dithered_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        self.original_frame.columnconfigure(0, weight=1)
        self.original_frame.rowconfigure(0, weight=1)
        self.dithered_frame.columnconfigure(0, weight=1)
        self.dithered_frame.rowconfigure(0, weight=1)
    
    def create_info_panel(self, parent):
        """Create the right info and settings panel"""
        info_frame = ttk.LabelFrame(parent, text="Information", padding="10")
        info_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Image info
        ttk.Label(info_frame, text="Image Information:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.image_info_text = ScrolledText(info_frame, height=8, width=25, wrap=tk.WORD)
        self.image_info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Settings
        ttk.Label(info_frame, text="Settings:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Resize option
        self.resize_var = tk.BooleanVar(value=True)
        resize_check = ttk.Checkbutton(info_frame, text="Resize to 128x128 (Minecraft map size)",
                                      variable=self.resize_var)
        resize_check.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Palette info
        ttk.Separator(info_frame, orient='horizontal').grid(row=4, column=0, 
                                                           sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(info_frame, text="Palette:", font=('Arial', 10, 'bold')).grid(
            row=5, column=0, sticky=tk.W)
        
        palette_label = ttk.Label(info_frame, text=self.palette_info, wraplength=200)
        palette_label.grid(row=6, column=0, sticky=tk.W, pady=(0, 10))
        
        # Algorithm info
        ttk.Label(info_frame, text="Algorithm:", font=('Arial', 10, 'bold')).grid(
            row=7, column=0, sticky=tk.W)
        
        algorithm_label = ttk.Label(info_frame, text="Floyd-Steinberg Error Diffusion\nLAB Color Space", 
                                   wraplength=200)
        algorithm_label.grid(row=8, column=0, sticky=tk.W)
        
        # Configure grid weights
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(1, weight=1)
        
        # Initialize image info
        self.update_image_info("No image loaded")
    
    def create_status_panel(self, parent):
        """Create the bottom status and progress panel"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Configure grid weights
        status_frame.columnconfigure(0, weight=1)
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        # Bind drag and drop events to the original image label
        self.original_label.bind("<Button-1>", self.on_click)
        self.original_label.bind("<B1-Motion>", self.on_drag)
        self.original_label.bind("<ButtonRelease-1>", self.on_drop)
        
        # For now, we'll use click to load since tkinter doesn't have built-in drag-drop
        self.original_label.bind("<Double-Button-1>", lambda e: self.load_image())
    
    def on_click(self, event):
        """Handle click on image area"""
        pass
    
    def on_drag(self, event):
        """Handle drag over image area"""
        pass
    
    def on_drop(self, event):
        """Handle drop on image area"""
        # For now, just trigger load dialog
        self.load_image()
    
    def load_image(self):
        """Load an image file"""
        if self.processing:
            messagebox.showwarning("Processing", "Please wait for current operation to complete.")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load image
                self.current_image = ImageProcessor.load_image(file_path)
                
                if self.current_image:
                    # Update preview
                    self.update_original_preview()
                    
                    # Update image info
                    info = ImageProcessor.get_image_info(self.current_image)
                    self.update_image_info(f"File: {Path(file_path).name}\n"
                                         f"Size: {info['width']}x{info['height']} pixels\n"
                                         f"Mode: {info['mode']}\n"
                                         f"Format: {info['format']}\n"
                                         f"Total pixels: {info['total_pixels']:,}")
                    
                    # Enable dither button
                    self.dither_btn.config(state='normal')
                    self.comparison_btn.config(state='normal')
                    
                    self.status_var.set(f"Loaded: {Path(file_path).name}")
                else:
                    messagebox.showerror("Error", "Failed to load image")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def update_original_preview(self):
        """Update the original image preview"""
        if self.current_image:
            # Create thumbnail for preview
            preview_image = self.current_image.copy()
            preview_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.original_preview = ImageTk.PhotoImage(preview_image)
            
            # Update label
            self.original_label.config(image=self.original_preview, text="")
    
    def update_dithered_preview(self):
        """Update the dithered image preview"""
        if self.dithered_image:
            # Create thumbnail for preview
            preview_image = self.dithered_image.copy()
            preview_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.dithered_preview = ImageTk.PhotoImage(preview_image)
            
            # Update label
            self.dithered_label.config(image=self.dithered_preview, text="")
            
            # Switch to dithered tab
            self.notebook.select(1)
    
    def update_image_info(self, info_text):
        """Update the image information display"""
        self.image_info_text.delete(1.0, tk.END)
        self.image_info_text.insert(1.0, info_text)
    
    def start_dithering(self):
        """Start the dithering process in a separate thread"""
        if not self.current_image or self.processing:
            return
        
        self.processing = True
        self.dither_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("Dithering in progress...")
        
        # Start dithering in separate thread
        thread = threading.Thread(target=self.dither_worker)
        thread.daemon = True
        thread.start()
    
    def dither_worker(self):
        """Worker function for dithering (runs in separate thread)"""
        try:
            # Set up progress callback
            def progress_callback(current, total):
                percent = (current / total) * 100
                self.progress_queue.put(percent)
            
            self.ditherer.set_progress_callback(progress_callback)
            
            # Perform dithering
            start_time = time.time()
            dithered = self.ditherer.dither_image(
                self.current_image, 
                resize_for_minecraft=self.resize_var.get()
            )
            end_time = time.time()
            
            # Put result in queue
            self.result_queue.put({
                'type': 'dither_complete',
                'image': dithered,
                'time': end_time - start_time
            })
            
        except Exception as e:
            self.result_queue.put({
                'type': 'error',
                'message': str(e)
            })
    
    def generate_comparison(self):
        """Generate comparison images (original, quantized, dithered)"""
        if not self.current_image or self.processing:
            return
        
        self.processing = True
        self.comparison_btn.config(state='disabled')
        self.status_var.set("Generating comparison images...")
        
        # Start comparison in separate thread
        thread = threading.Thread(target=self.comparison_worker)
        thread.daemon = True
        thread.start()
    
    def comparison_worker(self):
        """Worker function for comparison generation"""
        try:
            # Set up progress callback
            def progress_callback(current, total):
                percent = (current / total) * 100
                self.progress_queue.put(percent)
            
            self.ditherer.set_progress_callback(progress_callback)
            
            # Generate comparison
            original, quantized, dithered = self.ditherer.dither_with_comparison(
                self.current_image,
                resize_for_minecraft=self.resize_var.get()
            )
            
            # Save comparison images
            timestamp = int(time.time())
            base_name = f"comparison_{timestamp}"
            
            original.save(f"{base_name}_original.png")
            quantized.save(f"{base_name}_quantized.png")
            dithered.save(f"{base_name}_dithered.png")
            
            self.result_queue.put({
                'type': 'comparison_complete',
                'image': dithered,
                'files': [f"{base_name}_original.png", f"{base_name}_quantized.png", f"{base_name}_dithered.png"]
            })
            
        except Exception as e:
            self.result_queue.put({
                'type': 'error',
                'message': str(e)
            })
    
    def show_palette_preview(self):
        """Show palette preview in a new window"""
        try:
            # Generate palette preview
            preview_path = "temp_palette_preview.png"
            if self.ditherer.save_palette_preview(preview_path):
                # Create new window
                palette_window = tk.Toplevel(self.root)
                palette_window.title("Color Palette Preview")
                palette_window.geometry("300x400")
                
                # Load and display palette image
                palette_img = Image.open(preview_path)
                palette_img = palette_img.resize((250, 250), Image.Resampling.NEAREST)
                palette_photo = ImageTk.PhotoImage(palette_img)
                
                palette_label = ttk.Label(palette_window, image=palette_photo)
                palette_label.image = palette_photo  # Keep a reference
                palette_label.pack(pady=20)
                
                # Add info
                info_text = f"Palette: {len(self.ditherer.palette.CARPET_COLORS)} colors\n"
                info_text += "Algorithm: Floyd-Steinberg Error Diffusion\n"
                info_text += "Color Space: LAB (perceptual)"
                
                info_label = ttk.Label(palette_window, text=info_text, justify='center')
                info_label.pack(pady=10)
                
                # Clean up temp file
                os.remove(preview_path)
            else:
                messagebox.showerror("Error", "Failed to generate palette preview")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show palette preview: {str(e)}")
    
    def save_image(self):
        """Save the dithered image"""
        if not self.dithered_image:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Dithered Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.dithered_image.save(file_path)
                self.status_var.set(f"Saved: {Path(file_path).name}")
                messagebox.showinfo("Success", f"Image saved successfully:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def monitor_progress(self):
        """Monitor progress and results from worker threads"""
        try:
            # Check for progress updates
            while not self.progress_queue.empty():
                progress = self.progress_queue.get_nowait()
                self.progress_var.set(progress)
            
            # Check for results
            while not self.result_queue.empty():
                result = self.result_queue.get_nowait()
                
                if result['type'] == 'dither_complete':
                    self.dithered_image = result['image']
                    self.update_dithered_preview()
                    self.save_btn.config(state='normal')
                    self.status_var.set(f"Dithering complete! ({result['time']:.2f}s)")
                    self.processing = False
                    self.dither_btn.config(state='normal')
                    self.comparison_btn.config(state='normal')
                    
                elif result['type'] == 'comparison_complete':
                    self.dithered_image = result['image']
                    self.update_dithered_preview()
                    self.save_btn.config(state='normal')
                    files_str = '\n'.join(result['files'])
                    messagebox.showinfo("Comparison Complete", 
                                      f"Comparison images saved:\n{files_str}")
                    self.status_var.set("Comparison generation complete!")
                    self.processing = False
                    self.comparison_btn.config(state='normal')
                    
                elif result['type'] == 'error':
                    messagebox.showerror("Error", f"Processing failed: {result['message']}")
                    self.status_var.set("Error occurred")
                    self.processing = False
                    self.dither_btn.config(state='normal')
                    self.comparison_btn.config(state='normal')
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.monitor_progress)

def main():
    """Main function to start the GUI application"""
    root = tk.Tk()
    app = DithererGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 