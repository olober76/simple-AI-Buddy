import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time

class ResultPopup:
    def __init__(self, result, master, on_close=None):
        self.on_close = on_close
        self.root = tk.Toplevel(master)
        self.is_main = False
        self.root.title("Sang Petuah menjawab")
        self.root.geometry("1200x800")
        self.wav_filepath = None
        self.tts_thread = None
        self.tts_done = False

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
        image_path = "./app/assets/wizard.jpg"
        try:
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(main_frame, image=self.photo)
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            error_label = ttk.Label(main_frame, text="Image not available")
            error_label.pack(pady=20)

        # Display result text
        result_text = tk.Text(main_frame, wrap=tk.WORD, width=80, height=10, font=('Arial', 12))
        result_text.pack(pady=20, padx=20)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)

        # Disable close button until TTS done + 2s
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.can_close = False

        # Jalankan TTS di thread terpisah
        self.tts_thread = threading.Thread(target=self.run_tts_and_timer, args=(result,), daemon=True)
        self.tts_thread.start()

    def run_tts_and_timer(self, text):
        from app.service.tts_exec import synthesize_and_play
        print("LOG : TTS - Starting TTS...")
        duration, filepath = synthesize_and_play(text)
        self.wav_filepath = filepath
        self.tts_done = True
        # Hapus file setelah play
        if os.path.exists(filepath):
            os.remove(filepath)
        # Tunggu 2 detik setelah suara selesai
        time.sleep(2)
        self.can_close = True
        # Tutup otomatis setelah 2 detik selesai, jika belum ditutup manual
        if self.root.winfo_exists():
            self.root.after(0, self.close_window)

    def close_window(self):
        # Jika user menutup manual sebelum TTS selesai, hentikan thread TTS (tidak bisa force kill, tapi lanjutkan close)
        if not self.can_close:
            # Jika file wav sudah ada, hapus
            if self.wav_filepath and os.path.exists(self.wav_filepath):
                try:
                    print(f"LOG : TTS - Removing wav: {self.wav_filepath}")
                    os.remove(self.wav_filepath)
                except Exception as e:
                    print(f"Error removing wav: {e}")
            self.can_close = True  # Supaya tidak double close
        try:
            if self.root.winfo_exists():
                self.root.destroy()
            if self.on_close:
                self.on_close()
        except Exception as e:
            print(f"Error closing window: {e}")

def show_result_popup(result, master, on_close=None):
    popup = ResultPopup(result, master, on_close)
    return popup
