import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ResultPopup:
    def __init__(self, result):
        self.root = tk.Tk()
        self.root.title("Sang Petuah menjawab")
        self.root.geometry("1200x800")
        
        # Configure window to be centered
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Load and display image using direct relative path
        image_path = "./assets/wizard.jpg"
        try:
            # Load and resize image
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)  # Keep reference as instance variable
            
            image_label = ttk.Label(main_frame, image=self.photo)
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Create a placeholder label if image fails to load
            error_label = ttk.Label(main_frame, text="Image not available")
            error_label.pack(pady=20)
        
        # Display result text
        result_text = tk.Text(main_frame, wrap=tk.WORD, width=80, height=10, font=('Arial', 12))
        result_text.pack(pady=20, padx=20)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)  # Make text read-only
        
        # Add window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Schedule window close after 20 seconds
        self.timer_id = self.root.after(20000, self.close_window)
        
        # Start the main loop
        self.root.mainloop()
    
    def close_window(self):
        try:
            # Cancel the timer if it exists
            if hasattr(self, 'timer_id'):
                self.root.after_cancel(self.timer_id)
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error closing window: {e}")

def show_result_popup(result):
    popup = ResultPopup(result)
