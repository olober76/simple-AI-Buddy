import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time

class ResultPopup:
    def __init__(self, result, master, audio_filepath=None, on_close=None):
        self.on_close = on_close
        self.root = tk.Toplevel(master)
        self.is_main = False
        self.root.title("🧙‍♂️ The Wizard's Wisdom")
        self.root.geometry("1700x1000")
        self.wav_filepath = audio_filepath
        self.audio_filepath = audio_filepath
        self.tts_thread = None
        self.tts_done = True  # Set to True since audio is already processed
        
        # Medieval color palette
        self.colors = {
            'bg_dark': '#1a0a1a',      # Very dark purple/black
            'bg_medium': '#2d1b2d',    # Dark purple
            'bg_light': '#3d2b3d',     # Medium purple
            'accent_gold': '#d4af37',  # Mystical gold
            'accent_silver': '#c0c0c0', # Silver
            'text_gold': '#f4e4a1',    # Light gold text
            'text_light': '#e8d5b7',   # Warm light text
            'border_magic': '#8b4b8b',  # Mystical purple border
            'shadow': '#0f0a0f'        # Deep shadow
        }

        # Configure main window style
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Configure window to be centered
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1700) // 2
        y = (screen_height - 1000) // 2
        self.root.geometry(f"1700x1000+{x}+{y}")

        # Create mystical styled main container
        self.create_mystical_ui(result)

        # Setup close button behavior
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.can_close = True  # Can close immediately since audio is ready

        # If audio file provided, schedule audio playback after GUI is shown
        if self.audio_filepath and os.path.exists(self.audio_filepath):
            # Delay audio playback to let GUI render first
            print(f"LOG : Scheduling audio playback in 500ms: {self.audio_filepath}")
            self.root.after(500, self.play_existing_audio)  # 500ms delay
        
        # Auto-close after audio duration + buffer time
        if self.audio_filepath:
            duration = self.get_audio_duration()
            auto_close_time = int((duration + 5) * 1000)  # duration + 5 seconds buffer (increased)
            print(f"LOG : Auto-close scheduled in {auto_close_time/1000:.1f} seconds")
            self.root.after(auto_close_time, self.close_window)
        else:
            # No audio, close after 8 seconds
            self.root.after(8000, self.close_window)
    
    def create_mystical_ui(self, result):
        """Create the mystical medieval-themed UI"""
        # Main container with mystical styling
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create ornate border frame
        border_frame = tk.Frame(
            main_container, 
            bg=self.colors['border_magic'],
            relief='raised',
            bd=3
        )
        border_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Inner mystical frame
        inner_frame = tk.Frame(
            border_frame, 
            bg=self.colors['bg_medium'],
            relief='sunken',
            bd=2
        )
        inner_frame.pack(expand=True, fill='both', padx=8, pady=8)
        
        # Title section with mystical header
        self.create_title_section(inner_frame)
        
        # Wizard image section
        self.create_wizard_section(inner_frame)
        
        # Mystical text display section
        self.create_text_section(inner_frame, result)
        
        # Mystical footer with magical symbols
        self.create_footer_section(inner_frame)
    
    def create_title_section(self, parent):
        """Create mystical title header"""
        title_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        title_frame.pack(fill='x', pady=(10, 5))
        title_frame.pack_propagate(False)
        
        # Magical symbols
        symbols_top = tk.Label(
            title_frame,
            text="✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_gold'],
            font=('Georgia', 12)
        )
        symbols_top.pack(pady=(5, 0))
        
        # Main title
        title_label = tk.Label(
            title_frame,
            text="🧙‍♂️ THE WIZARD'S ANCIENT WISDOM 🧙‍♂️",
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gold'],
            font=('Palatino Linotype', 18, 'bold')
        )
        title_label.pack(pady=2)
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="~ Mystical Knowledge from the Arcane Realms ~",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_silver'],
            font=('Georgia', 10, 'italic')
        )
        subtitle_label.pack()
    
    def create_wizard_section(self, parent):
        """Create wizard image section with mystical frame"""
        image_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        image_frame.pack(pady=10)
        
        # Ornate image border
        image_border = tk.Frame(
            image_frame,
            bg=self.colors['accent_gold'],
            relief='raised',
            bd=4
        )
        image_border.pack()
        
        # Load and display wizard image
        image_path = "./app/assets/wizard.jpg"
        try:
            image = Image.open(image_path)
            image = image.resize((350, 350), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(
                image_border, 
                image=self.photo,
                bg=self.colors['bg_dark'],
                relief='sunken',
                bd=2
            )
            image_label.pack(padx=6, pady=6)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Fallback mystical placeholder
            placeholder = tk.Label(
                image_border,
                text="🔮\n✨ MYSTICAL WIZARD ✨\n🔮",
                bg=self.colors['bg_dark'],
                fg=self.colors['text_gold'],
                font=('Georgia', 24, 'bold'),
                relief='sunken',
                bd=2,
                width=20,
                height=10
            )
            placeholder.pack(padx=6, pady=6)
    
    def create_text_section(self, parent, result):
        """Create mystical text display section"""
        text_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        text_frame.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Ornate text border
        text_border = tk.Frame(
            text_frame,
            bg=self.colors['border_magic'],
            relief='raised',
            bd=3
        )
        text_border.pack(expand=True, fill='both')
        
        # Inner text container
        text_container = tk.Frame(
            text_border,
            bg=self.colors['bg_light'],
            relief='sunken',
            bd=2
        )
        text_container.pack(expand=True, fill='both', padx=4, pady=4)
        
        # Scrollable text widget with mystical styling
        text_widget = tk.Text(
            text_container,
            wrap=tk.WORD,
            width=70,
            height=8,
            font=('Georgia', 13, 'normal'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light'],
            selectbackground=self.colors['accent_gold'],
            selectforeground=self.colors['bg_dark'],
            relief='flat',
            bd=0,
            padx=20,
            pady=15,
            insertbackground=self.colors['text_gold'],
            highlightthickness=0
        )
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add scrollbar with mystical styling
        scrollbar = tk.Scrollbar(
            text_container, 
            command=text_widget.yview,
            bg=self.colors['bg_medium'],
            troughcolor=self.colors['bg_dark'],
            activebackground=self.colors['accent_gold']
        )
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Insert and style the text
        text_widget.insert(tk.END, result)
        text_widget.config(state=tk.DISABLED)
    
    def create_footer_section(self, parent):
        """Create mystical footer with magical elements"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=60)
        footer_frame.pack(fill='x', pady=(5, 10))
        footer_frame.pack_propagate(False)
        
        # Magical symbols bottom
        symbols_bottom = tk.Label(
            footer_frame,
            text="⋆ ✦ ⋆ ✧ ⋆ May this wisdom guide your path ⋆ ✧ ⋆ ✦ ⋆",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_silver'],
            font=('Georgia', 11, 'italic')
        )
        symbols_bottom.pack(pady=5)
        
        # Mystical closing
        closing_label = tk.Label(
            footer_frame,
            text="✨ Blessed by Ancient Magic ✨",
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_gold'],
            font=('Palatino Linotype', 10, 'bold')
        )
        closing_label.pack()
        
        # Add magical pulsing effect to title
        self.start_magical_effects()
    
    def start_magical_effects(self):
        """Add subtle magical animations"""
        # This could be expanded with more complex animations
        # For now, just ensure smooth rendering
        self.root.update_idletasks()
        
        # Add a subtle fade-in effect by adjusting window attributes
        try:
            self.root.attributes('-alpha', 0.0)  # Start transparent
            self.fade_in()
        except tk.TclError:
            # If fade effects not supported, just show normally
            pass
    
    def fade_in(self, alpha=0.0):
        """Create smooth fade-in effect"""
        if alpha < 1.0:
            alpha += 0.05
            try:
                self.root.attributes('-alpha', alpha)
                self.root.after(30, lambda: self.fade_in(alpha))
            except tk.TclError:
                # Fallback if transparency not supported
                self.root.attributes('-alpha', 1.0)
        
    def play_existing_audio(self):
        """Play the pre-processed audio file in background thread"""
        print(f"LOG : Starting audio playback: {self.audio_filepath}")
        
        # Play audio in background thread to avoid blocking GUI
        def play_audio_background():
            audio_played = self.play_with_system_player()
            
            if not audio_played:
                print("LOG : Warning - Could not play audio with any method")
                # Still schedule cleanup for failed audio
                self.root.after(2000, self.cleanup_audio)
            else:
                print("LOG : Audio playback completed successfully")
                # Schedule cleanup after audio finishes + buffer
                duration = self.get_audio_duration()
                cleanup_delay = max(3000, int(duration * 1000) + 1000)  # At least 3 seconds or duration + 1s
                print(f"LOG : Scheduling audio cleanup in {cleanup_delay/1000:.1f} seconds")
                self.root.after(cleanup_delay, self.cleanup_audio)
        
        # Start audio in separate thread
        audio_thread = threading.Thread(target=play_audio_background, daemon=True)
        audio_thread.start()
        print("LOG : Audio playback thread started")
    
    def get_audio_duration(self) -> float:
        """Get audio file duration"""
        try:
            import subprocess
            # Try ffprobe first
            result = subprocess.run(['ffprobe', '-i', self.audio_filepath, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        
        try:
            # Try sox as fallback
            result = subprocess.run(['soxi', '-D', self.audio_filepath], capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        
        # Default estimate
        try:
            file_size = os.path.getsize(self.audio_filepath)
            return max(3.0, file_size / 32000)  # Rough estimate
        except:
            return 5.0  # Default fallback
            
    def play_with_system_player(self):
        """Fallback to system audio players (NON-BLOCKING)"""
        import subprocess
        audio_players = [
            ['paplay', self.audio_filepath],           # PulseAudio
            ['aplay', self.audio_filepath],            # ALSA  
            ['ffplay', '-nodisp', '-autoexit', self.audio_filepath],  # FFmpeg
            ['mpv', '--no-video', self.audio_filepath], # MPV
        ]
        
        for player_cmd in audio_players:
            try:
                print(f"LOG : Trying to play audio with: {player_cmd[0]}")
                # Use Popen instead of run to make it non-blocking
                process = subprocess.Popen(player_cmd, 
                                         stdout=subprocess.DEVNULL, 
                                         stderr=subprocess.DEVNULL)
                print(f"LOG : Audio started with {player_cmd[0]} (PID: {process.pid})")
                
                # Wait for process to complete (this will block this thread only, not GUI)
                process.wait()
                
                if process.returncode == 0:
                    print(f"LOG : Audio played successfully with {player_cmd[0]}")
                    return True
                else:
                    print(f"LOG : {player_cmd[0]} exited with code {process.returncode}")
                    
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"LOG : {player_cmd[0]} failed: {e}")
                continue
        
        return False
                
    def cleanup_audio(self):
        """Clean up audio file after playback"""
        if self.audio_filepath and os.path.exists(self.audio_filepath):
            try:
                os.remove(self.audio_filepath)
                print(f"LOG : Audio file cleaned up: {self.audio_filepath}")
            except Exception as e:
                print(f"LOG : Error cleaning up audio: {e}")
        else:
            print(f"LOG : Audio file already cleaned up or not found: {self.audio_filepath}")

    def close_window(self):
        # Clean up any remaining audio files
        if self.audio_filepath and os.path.exists(self.audio_filepath):
            try:
                print(f"LOG : Removing remaining audio file: {self.audio_filepath}")
                os.remove(self.audio_filepath)
            except Exception as e:
                print(f"LOG : Error removing audio file: {e}")
                
        try:
            if self.root.winfo_exists():
                self.root.destroy()
            if self.on_close:
                self.on_close()
        except Exception as e:
            print(f"LOG : Error closing window: {e}")

def show_result_popup(result, master, audio_filepath=None, on_close=None):
    """Show result popup with optional pre-processed audio file"""
    popup = ResultPopup(result, master, audio_filepath, on_close)
    return popup
