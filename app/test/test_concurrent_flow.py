#!/usr/bin/env python3
"""
Test script untuk menguji concurrent audio dan GUI flow
"""

import sys
import os
import tkinter as tk
import threading
import time

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

def test_concurrent_flow():
    """Test concurrent GUI and audio flow"""
    root = tk.Tk()
    root.title("Test Concurrent Audio & GUI")
    root.geometry("400x250")
    
    # Center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 250) // 2
    root.geometry(f"400x250+{x}+{y}")
    
    def test_flow():
        from app.utils.gui_Loading_Wizard import show_wizard_loading
        
        # Step 1: Show loading
        print("TEST : Step 1 - Showing loading window...")
        loading = show_wizard_loading(root)
        
        # Step 2: Simulate audio generation
        def simulate_processing():
            print("TEST : Step 2 - Simulating TTS processing...")
            time.sleep(2)  # Simulate TTS processing
            
            # Create dummy audio file for testing
            dummy_audio = "./app/temp/test_audio.wav"
            os.makedirs("./app/temp", exist_ok=True)
            
            # Create a simple dummy wav file (silence)
            import wave
            with wave.open(dummy_audio, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(22050)  # Sample rate
                # Write 3 seconds of silence
                silence = b'\\x00\\x00' * 22050 * 3
                wav_file.writeframes(silence)
            
            def show_result():
                print("TEST : Step 3 - Closing loading window...")
                loading.close_loading()
                
                def show_popup():
                    print("TEST : Step 4 - Showing result popup with audio...")
                    from app.utils.gui_Pop_Up_result import show_result_popup
                    show_result_popup(
                        "Test Result: This popup should appear FIRST, then audio should play in background!", 
                        root, 
                        dummy_audio
                    )
                    print("TEST : Step 5 - Popup created, audio should start playing shortly...")
                
                root.after(100, show_popup)
            
            root.after(0, show_result)
        
        # Start processing in thread
        processing_thread = threading.Thread(target=simulate_processing, daemon=True)
        processing_thread.start()
    
    # Create test button
    test_btn = tk.Button(
        root, 
        text="Test Concurrent Flow",
        command=test_flow,
        font=('Arial', 12),
        pady=10
    )
    test_btn.pack(pady=20)
    
    info_label = tk.Label(
        root,
        text="Expected Flow:\\n1. Loading Window\\n2. Loading Closes\\n3. Popup Appears\\n4. Audio Plays Concurrently",
        font=('Arial', 9),
        fg='gray',
        justify='left'
    )
    info_label.pack(pady=10)
    
    # Auto-start test
    root.after(1000, test_flow)
    
    root.mainloop()

if __name__ == "__main__":
    test_concurrent_flow()