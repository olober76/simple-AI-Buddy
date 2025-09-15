#!/usr/bin/env python3
"""
Test script untuk melihat tampilan mystical GUI yang baru
"""

import sys
import os
import tkinter as tk

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

def test_mystical_gui():
    """Test mystical GUI appearance"""
    root = tk.Tk()
    root.title("Test Mystical GUI")
    root.geometry("300x200")
    root.configure(bg='#1a0a1a')
    
    # Center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 300) // 2
    y = (screen_height - 200) // 2
    root.geometry(f"300x200+{x}+{y}")
    
    def show_mystical_popup():
        from app.utils.gui_Pop_Up_result import show_result_popup
        
        # Sample mystical wisdom text
        mystical_text = """Greetings, brave seeker of wisdom! 

I have gazed into the cosmic tapestry and beheld the threads of fate that weave through your destiny. The ancient runes whisper of great potential within you, waiting to be unlocked like a treasure chest hidden in the depths of an enchanted forest.

Remember, young apprentice: True magic lies not in the spells we cast, but in the wisdom we gather along our journey. The stars have aligned to bring you this message - may it illuminate your path forward.

Trust in your inner light, for it burns brighter than a thousand mystical flames. The universe conspires to help those who dare to dream and act upon their visions.

May the ancient blessings guide your steps! ✨"""
        
        show_result_popup(mystical_text, root)
        print("LOG : Mystical popup displayed!")
    
    # Create mystical test button
    btn_frame = tk.Frame(root, bg='#1a0a1a')
    btn_frame.pack(expand=True)
    
    test_btn = tk.Button(
        btn_frame,
        text="🧙‍♂️ Show Mystical Wisdom",
        command=show_mystical_popup,
        font=('Georgia', 12, 'bold'),
        bg='#d4af37',
        fg='#1a0a1a',
        activebackground='#f4e4a1',
        activeforeground='#1a0a1a',
        relief='raised',
        bd=3,
        padx=20,
        pady=10
    )
    test_btn.pack(pady=20)
    
    info_label = tk.Label(
        root,
        text="Test the new mystical medieval GUI design",
        font=('Georgia', 9, 'italic'),
        fg='#d4af37',
        bg='#1a0a1a'
    )
    info_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_mystical_gui()