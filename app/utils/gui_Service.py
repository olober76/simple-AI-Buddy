import threading
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import PhotoImage, font
from app.utils.capture_the_voice import record_with_silence_detection


class AIAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧙‍♂️ The Mystical Voice Oracle")
        self.root.geometry("1700x1000")
        
        # Mystical color palette (same as result popup)
        self.colors = {
            'bg_dark': '#1a0a1a',      # Very dark purple/black
            'bg_medium': '#2d1b2d',    # Dark purple
            'bg_light': '#3d2b3d',     # Medium purple
            'accent_gold': '#d4af37',  # Mystical gold
            'accent_silver': '#c0c0c0', # Silver
            'text_gold': '#f4e4a1',    # Light gold text
            'text_light': '#e8d5b7',   # Warm light text
            'border_magic': '#8b4b8b',  # Mystical purple border
            'shadow': '#0f0a0f',       # Deep shadow
            'magic_glow': '#9d4edd',   # Magic glow effect
            'recording_red': '#ff6b6b'  # Recording indicator
        }
        
        # Configure main window mystical theme
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1700) // 2
        y = (screen_height - 1000) // 2
        self.root.geometry(f"1700x1000+{x}+{y}")

        self.recording = False
        self.transcription_callback = None

        # Create mystical UI components
        self.create_mystical_interface()

    def create_mystical_interface(self):
        """Create the main mystical interface"""
        # Main mystical container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create mystical border frame
        border_frame = tk.Frame(
            main_container,
            bg=self.colors['border_magic'],
            relief='raised',
            bd=4
        )
        border_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Inner mystical container
        inner_frame = tk.Frame(
            border_frame,
            bg=self.colors['bg_medium'],
            relief='sunken',
            bd=3
        )
        inner_frame.pack(expand=True, fill='both', padx=8, pady=8)
        
        # Create sections
        self.create_mystical_header(inner_frame)
        self.create_voice_capture_area(inner_frame)
        self.create_mystical_footer(inner_frame)
    
    def create_mystical_header(self, parent):
        """Create mystical header with wizard greeting"""
        header_container = tk.Frame(parent, bg=self.colors['bg_medium'], height=200)
        header_container.pack(fill='x', pady=(20, 10))
        header_container.pack_propagate(False)
        
        # Top magical symbols
        symbols_frame = tk.Frame(header_container, bg=self.colors['bg_medium'])
        symbols_frame.pack(pady=(10, 0))
        
        top_symbols = tk.Label(
            symbols_frame,
            text="✦ ✧ ⋆ ✨ ⋆ ✧ ✦ ✧ ⋆ ✨ ⋆ ✧ ✦",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_gold'],
            font=('Georgia', 14)
        )
        top_symbols.pack()
        
        # Main title
        title_label = tk.Label(
            header_container,
            text="🧙‍♂️ THE MYSTICAL VOICE ORACLE 🧙‍♂️",
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gold'],
            font=('Palatino Linotype', 24, 'bold')
        )
        title_label.pack(pady=(5, 2))
        
        # Subtitle with mystical greeting
        subtitle_label = tk.Label(
            header_container,
            text="~ Speak Your Heart's Desire to the Ancient Wisdom ~",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_silver'],
            font=('Georgia', 12, 'italic')
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Wizard icon section
        wizard_frame = tk.Frame(header_container, bg=self.colors['bg_medium'])
        wizard_frame.pack(pady=10)
        
        # Try to load wizard icon or use emoji
        try:
            wizard_img = Image.open("./app/assets/wizard.jpg").resize((80, 80), Image.Resampling.LANCZOS)
            self.wizard_icon = ImageTk.PhotoImage(wizard_img)
            
            # Create ornate frame for wizard icon
            wizard_border = tk.Frame(
                wizard_frame,
                bg=self.colors['accent_gold'],
                relief='raised',
                bd=3
            )
            wizard_border.pack()
            
            wizard_icon_label = tk.Label(
                wizard_border,
                image=self.wizard_icon,
                bg=self.colors['bg_dark'],
                relief='sunken',
                bd=2
            )
            wizard_icon_label.pack(padx=4, pady=4)
            
        except Exception as e:
            print(f"Could not load wizard image: {e}")
            # Fallback to emoji
            wizard_emoji = tk.Label(
                wizard_frame,
                text="🧙‍♂️",
                bg=self.colors['bg_medium'],
                font=('Georgia', 48)
            )
            wizard_emoji.pack()
        
        # Greeting message
        self.greeting_label = tk.Label(
            header_container,
            text="✨ Greetings, seeker of wisdom! Speak and I shall listen... ✨",
            bg=self.colors['bg_medium'],
            fg=self.colors['text_light'],
            font=('Georgia', 14, 'italic')
        )
        self.greeting_label.pack(pady=5)
        
        # Voice selection controls
        voice_controls = tk.Frame(header_container, bg=self.colors['bg_medium'])
        voice_controls.pack(pady=(10, 0))
        
        # Voice selection button
        self.voice_button = tk.Button(
            voice_controls,
            text="🎭 Choose Wizard Voice",
            font=('Cinzel', 10, 'bold'),
            fg='white',
            bg=self.colors['border_magic'],
            activebackground=self.colors['accent_gold'],
            relief='raised',
            bd=2,
            cursor='hand2',
            command=self.open_voice_selection,
            padx=15,
            pady=5
        )
        self.voice_button.pack(side='left', padx=(0, 10))
        
        # Current voice display
        from app.config.config import WizardVoices
        current_voice_info = WizardVoices.get_current_voice_info()
        self.voice_status_label = tk.Label(
            voice_controls,
            text=f"🧙‍♂️ Current Voice: {current_voice_info['name']}",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_silver'],
            font=('Georgia', 10, 'italic')
        )
        self.voice_status_label.pack(side='left')
    
    def create_voice_capture_area(self, parent):
        """Create mystical voice capture area"""
        # Voice capture container
        voice_container = tk.Frame(parent, bg=self.colors['bg_medium'])
        voice_container.pack(expand=True, fill='both', pady=20)
        
        # Mystical instruction
        instruction_label = tk.Label(
            voice_container,
            text="🎙️ Click the Enchanted Orb to Begin Your Mystical Query 🎙️",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_gold'],
            font=('Georgia', 16, 'bold')
        )
        instruction_label.pack(pady=(20, 30))
        
        # Microphone area with mystical styling
        mic_container = tk.Frame(voice_container, bg=self.colors['bg_medium'])
        mic_container.pack(expand=True)
        
        # Mystical orb border for microphone
        self.mic_border = tk.Frame(
            mic_container,
            bg=self.colors['accent_gold'],
            relief='raised',
            bd=6
        )
        self.mic_border.pack(pady=20)
        
        # Inner mystical frame for mic
        mic_inner = tk.Frame(
            self.mic_border,
            bg=self.colors['bg_dark'],
            relief='sunken',
            bd=4
        )
        mic_inner.pack(padx=8, pady=8)
        
        # Load microphone image
        try:
            mic_img = Image.open("./app/assets/mic.png").resize((150, 150), Image.Resampling.LANCZOS)
            self.original_mic_img = mic_img
            self.mic_photo = ImageTk.PhotoImage(mic_img)
            
            self.mic_button = tk.Label(
                mic_inner,
                image=self.mic_photo,
                bg=self.colors['bg_dark'],
                cursor="hand2"
            )
            self.mic_button.pack(padx=15, pady=15)
            self.mic_button.bind("<Button-1>", self.on_mic_click)
            
        except Exception as e:
            print(f"Could not load mic image: {e}")
            # Fallback microphone
            self.mic_button = tk.Label(
                mic_inner,
                text="🎤\nSPEAK",
                bg=self.colors['bg_dark'],
                fg=self.colors['accent_gold'],
                font=('Georgia', 24, 'bold'),
                cursor="hand2",
                width=10,
                height=5
            )
            self.mic_button.pack(padx=15, pady=15)
            self.mic_button.bind("<Button-1>", self.on_mic_click)
        
        # Processing/status label with mystical styling
        self.processing_label = tk.Label(
            voice_container,
            text="",
            font=('Georgia', 14, 'italic'),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gold']
        )
        self.processing_label.pack(pady=10)
    
    def create_mystical_footer(self, parent):
        """Create mystical footer"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        footer_frame.pack(fill='x', pady=(10, 20))
        footer_frame.pack_propagate(False)
        
        # Mystical instruction
        instruction = tk.Label(
            footer_frame,
            text="⚡ The ancient magic awaits your voice ⚡",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_silver'],
            font=('Georgia', 12, 'italic')
        )
        instruction.pack(pady=10)
        
        # Bottom symbols
        bottom_symbols = tk.Label(
            footer_frame,
            text="✨ ⋆ ✦ ⋆ ✧ ⋆ May wisdom flow through your words ⋆ ✧ ⋆ ✦ ⋆ ✨",
            bg=self.colors['bg_medium'],
            fg=self.colors['border_magic'],
            font=('Georgia', 10, 'italic')
        )
        bottom_symbols.pack()

    def set_transcription_callback(self, callback):
        self.transcription_callback = callback
        return self

    def on_mic_click(self, event):
        if self.recording:
            return

        self.recording = True
        
        # Update mystical processing message
        self.processing_label.config(
            text="🔮 The mystical orb is listening to your voice... 🔮",
            fg=self.colors['recording_red']
        )
        
        # Change mic border to indicate recording
        self.mic_border.config(bg=self.colors['recording_red'])
        
        # Start mystical animation
        self.animate_mystical_mic(1.0, 1.3, steps=8, grow=True)

        def on_record_complete(filepath):
            self.recording = False
            
            # Reset mic border color
            self.mic_border.config(bg=self.colors['accent_gold'])
            
            # Update status message
            if filepath:
                self.root.after(0, lambda: self.processing_label.config(
                    text="✨ Your voice has been captured by ancient magic... ✨",
                    fg=self.colors['text_gold']
                ))
            else:
                self.root.after(0, lambda: self.processing_label.config(
                    text="⚠️ The magical energies could not capture your voice... ⚠️",
                    fg=self.colors['recording_red']
                ))

        def process_recording():
            result = record_with_silence_detection(on_complete=on_record_complete)
            if self.transcription_callback and result:
                # Update message for processing
                self.root.after(0, lambda: self.processing_label.config(
                    text="🧙‍♂️ The wizard is pondering your request... 🧙‍♂️",
                    fg=self.colors['magic_glow']
                ))
                
                # Jalankan callback di thread utama untuk menghindari masalah threading
                self.root.after(0, lambda: self.transcription_callback(result))

        threading.Thread(target=process_recording, daemon=True).start()

    def animate_mystical_mic(self, current, target, steps=8, grow=True):
        """Enhanced mystical microphone animation"""
        if steps == 0:
            return

        scale = current + (target - current) / steps
        
        # Only animate if we have the original image
        if hasattr(self, 'original_mic_img'):
            new_size = int(150 * scale)  # Base size 150
            resized = self.original_mic_img.resize((new_size, new_size), Image.Resampling.LANCZOS)
            self.mic_photo = ImageTk.PhotoImage(resized)
            self.mic_button.configure(image=self.mic_photo)
        
        # Add pulsing effect to border during recording
        if self.recording and steps % 2 == 0:
            # Alternate border colors for magical effect
            border_color = self.colors['magic_glow'] if steps % 4 == 0 else self.colors['recording_red']
            self.mic_border.config(bg=border_color)

        self.root.after(60, lambda: self.animate_mystical_mic(
            scale, 1.0 if grow else 1.3, steps - 1, not grow
        ))

    def show_popup_and_hide_main(self, result):
        # Sembunyikan window utama
        self.root.withdraw()
        # Import di sini untuk menghindari circular import
        from app.utils.gui_Pop_Up_result import show_result_popup

        def on_popup_close():
            self.root.deiconify()  # Tampilkan lagi window utama

        # Buat popup dengan callback close
        popup = show_result_popup(result, master=self.root, on_close=on_popup_close)
        
    def show_popup_and_hide_main_with_audio(self, result, audio_filepath):
        # Sembunyikan window utama
        self.root.withdraw()
        # Import di sini untuk menghindari circular import
        from app.utils.gui_Pop_Up_result import show_result_popup

        def on_popup_close():
            self.root.deiconify()  # Tampilkan lagi window utama

        # Buat popup dengan audio file dan callback close
        popup = show_result_popup(result, master=self.root, audio_filepath=audio_filepath, on_close=on_popup_close)
    
    def open_voice_selection(self):
        """Open the mystical voice selection window"""
        try:
            from app.utils.gui_Voice_Selection import VoiceSelectionWindow
            VoiceSelectionWindow(self.root)
        except Exception as e:
            print(f"Error opening voice selection: {e}")
            # Show error message to user
            error_label = tk.Label(
                self.root,
                text=f"❌ Could not open voice selection: {e}",
                fg='red',
                bg=self.colors['bg_medium']
            )
            error_label.pack(pady=5)
            self.root.after(3000, error_label.destroy)
    
    def update_voice_status(self, voice_name):
        """Update the voice status display"""
        self.voice_status_label.config(text=f"🧙‍♂️ Current Voice: {voice_name}")
        
        # Show confirmation message
        confirmation = tk.Label(
            self.root,
            text=f"✅ Voice changed to: {voice_name}",
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_medium'],
            font=('Georgia', 10, 'bold')
        )
        confirmation.pack(pady=2)
        
        # Remove confirmation after 3 seconds
        self.root.after(3000, confirmation.destroy)

