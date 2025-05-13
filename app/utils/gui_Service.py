import threading
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import PhotoImage, font
from app.utils.capture_the_voice import record_with_silence_detection


class AIAssistantApp:
    def __init__(self, root):
        # Coba buat font secara eksplisit
        self.inter_font = font.Font(family="Inter", size=20, weight="bold") # STILL DONT WORK 
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")

        self.recording = False
        self.transcription_callback = None

        # Frame untuk icon AI dan teks
        self.header_frame = tk.Frame(root, bg="white")
        self.header_frame.pack(pady=20)

        ai_img = Image.open("./app/assets/ai_icon.png").resize((64, 64), Image.Resampling.LANCZOS)
        self.ai_icon = ImageTk.PhotoImage(ai_img)

        self.ai_icon_label = tk.Label(self.header_frame, image=self.ai_icon, bg="white")
        self.ai_icon_label.pack(side=tk.LEFT, padx=(0, 10))

        self.greeting_label = tk.Label(self.header_frame, text="Hello, What can I do for you", font=(self.inter_font), bg="white")
        self.greeting_label.pack(side=tk.LEFT)

        # Processing label
        self.processing_label = tk.Label(root, text="", font=("Arial", 12), bg="white", fg="green")
        self.processing_label.pack()

        mic_img = Image.open("./app/assets/mic.png").resize((128, 128), Image.Resampling.LANCZOS)
        self.original_mic_img = mic_img
        self.mic_photo = ImageTk.PhotoImage(mic_img)

        self.mic_button = tk.Label(root, image=self.mic_photo, bg="white", cursor="hand2")
        self.mic_button.pack(pady=20)
        self.mic_button.bind("<Button-1>", self.on_mic_click)

    def set_transcription_callback(self, callback):
        self.transcription_callback = callback
        return self

    def on_mic_click(self, event):
        if self.recording:
            return

        self.recording = True
        self.processing_label.config(text="Processing...")
        self.animate_mic(1.0, 1.2, steps=5, grow=True)

        def on_record_complete(filepath):
            self.recording = False
            self.root.after(0, lambda: self.processing_label.config(
                text="Done Listening." if filepath else "Failed to Record."))

        def process_recording():
            result = record_with_silence_detection(on_complete=on_record_complete)
            if self.transcription_callback and result:
                # Jalankan callback di thread utama untuk menghindari masalah threading
                self.root.after(0, lambda: self.transcription_callback(result))

        threading.Thread(target=process_recording, daemon=True).start()

    def animate_mic(self, current, target, steps=5, grow=True):
        if steps == 0:
            return

        scale = current + (target - current) / steps
        new_size = int(128 * scale)
        resized = self.original_mic_img.resize((new_size, new_size), Image.Resampling.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(resized)
        self.mic_button.configure(image=self.mic_photo)
        self.mic_button.pack()

        self.root.after(30, lambda: self.animate_mic(scale, 1.0 if grow else 1.2, steps - 1, not grow))

    