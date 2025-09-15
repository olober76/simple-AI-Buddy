import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import os

class WizardLoadingWindow:
    def __init__(self, master, on_complete=None):
        self.on_complete = on_complete
        self.root = tk.Toplevel(master)
        self.root.title("Sang Petuah sedang berfikir...")
        self.root.geometry("1100x500")
        self.root.resizable(False, False)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1100) // 2  # Fixed: use 1100 not 900
        y = (screen_height - 500) // 2  # Fixed: use 500 not 800
        self.root.geometry(f"1100x500+{x}+{y}")

        # Make window stay on top and modal
        self.root.transient(master)
        self.root.grab_set()
        
        # Disable close button
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Configure background
        self.root.configure(bg='#2c3e50')
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Load wizard image
        self.setup_wizard_image(main_frame)
        
        # Loading text
        self.loading_text = tk.Label(
            main_frame,
            text="The Wizard is creating his wisdom...",
            font=('Arial', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.loading_text.pack(pady=(20, 10))
        
        # Subtitle text
        self.subtitle_text = tk.Label(
            main_frame,
            text="Preparing mystical audio response",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        self.subtitle_text.pack(pady=(0, 20))
        
        # Progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Wizard.Horizontal.TProgressbar",
            troughcolor='#34495e',
            background='#3498db',
            lightcolor='#3498db',
            darkcolor='#3498db'
        )
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            mode='indeterminate',
            style="Wizard.Horizontal.TProgressbar",
            length=400
        )
        self.progress_bar.pack(pady=10)
        
        # Status text that changes
        self.status_text = tk.Label(
            main_frame,
            text="Initializing...",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.status_text.pack(pady=10)
        
        # Start progress animation
        self.progress_bar.start(10)
        
        # Start status updates
        self.status_messages = [
            "Channeling mystical energies...",
            "Brewing wisdom in the cauldron...",
            "Consulting ancient scrolls...",
            "Weaving words of enlightenment...",
            "Enchanting voice with magic...",
            "Finalizing mystical response..."
        ]
        self.current_status = 0
        self.update_status()
        
    def setup_wizard_image(self, parent):
        """Load and display wizard image"""
        image_path = "./app/assets/wizard-thingking.png"
        try:
            image = Image.open(image_path)
            # Make it smaller for loading window
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(parent, image=self.photo, bg='#2c3e50')
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading wizard image: {e}")
            # Fallback - simple text wizard
            wizard_text = tk.Label(
                parent,
                text="🧙‍♂️",
                font=('Arial', 80),
                fg='#ecf0f1',
                bg='#2c3e50'
            )
            wizard_text.pack(pady=10)
    
    def update_status(self):
        """Update status message cyclically"""
        if hasattr(self, 'status_text') and self.status_text.winfo_exists():
            self.status_text.config(text=self.status_messages[self.current_status])
            self.current_status = (self.current_status + 1) % len(self.status_messages)
            # Update every 1.5 seconds
            self.root.after(1500, self.update_status)
    
    def close_loading(self):
        """Close loading window and call completion callback"""
        try:
            if self.root.winfo_exists():
                self.progress_bar.stop()
                self.root.grab_release()
                self.root.destroy()
            if self.on_complete:
                self.on_complete()
        except Exception as e:
            print(f"Error closing loading window: {e}")

def show_wizard_loading(master, on_complete=None):
    """Show wizard loading window"""
    loading = WizardLoadingWindow(master, on_complete)
    return loading