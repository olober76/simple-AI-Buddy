import os
import uuid
import time
import threading
import numpy as np
import tkinter as tk
import sounddevice as sd




from PIL import Image, ImageTk
from tkinter import PhotoImage, font
from scipy.io.wavfile import write as wav_write


class AIAssistantApp:
    def __init__(self, root):
        # Coba buat font secara eksplisit
        self.inter_font = font.Font(family="Inter", size=20, weight="bold") # STILL DONT WORK 
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")

        self.recording = False

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

    def on_mic_click(self, event):
        if self.recording:
            return  # mencegah klik berulang

        self.recording = True
        self.processing_label.config(text="Processing...")
        self.animate_mic(1.0, 1.2, steps=5, grow=True)

        threading.Thread(target=self.record_with_silence_detection, daemon=True).start()

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

    def record_with_silence_detection(self):
        duration_limit = 15
        silence_threshold = 0.01
        silence_duration = 2

        samplerate = 16000
        blocksize = 1024
        silent_start = None
        recorded_audio = []

        def callback(indata, frames, time_info, status):
            nonlocal silent_start
            volume_norm = np.linalg.norm(indata)
            recorded_audio.append(indata.copy())

            now = time.time()
            if volume_norm < silence_threshold:
                if silent_start is None:
                    silent_start = now
                elif now - silent_start >= silence_duration:
                    raise sd.CallbackStop
            else:
                silent_start = None

        try:
            with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, blocksize=blocksize):
                sd.sleep(int(duration_limit * 1000))
        except Exception as e:
            print("Rekaman Errors:", e)

        self.recording = False
        self.root.after(0, lambda: self.processing_label.config(text="Done Listening."))

        if recorded_audio:
            audio_data = np.concatenate(recorded_audio, axis=0)
            output_dir = "./app/temp"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{uuid.uuid4().hex}.wav"
            filepath = os.path.join(output_dir, filename)

            wav_write(filepath, samplerate, audio_data)
            print(f"Audio disimpan di: {filepath}")
        else:
            print("Tidak ada audio yang terekam.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistantApp(root)
    root.mainloop()
