import tkinter as tk
from tkinter import ttk
from app.config.config import WizardVoices
from app.service.tts_exec import TTS, synthesize_audio_only, play_audio_system
import threading
import os

class VoiceSelectionWindow:
    """🧙‍♂️ Mystical Voice Selection Window for choosing wizard voices"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.current_test_audio = None
        
        self.setup_window()
        self.create_mystical_interface()
        
    def setup_window(self):
        """Setup the mystical voice selection window"""
        self.window.title("🧙‍♂️ Mystical Voice Selection")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Mystical colors
        self.colors = {
            'bg_dark': '#1a0d26',      # Deep mystical purple
            'bg_medium': '#2d1b3d',    # Medium mystical purple
            'accent_gold': '#d4af37',   # Mystical gold
            'accent_purple': '#8a2be2', # Bright mystical purple
            'text_light': '#e6d7ff',   # Light mystical text
            'text_gold': '#ffd700',    # Gold text
            'border_mystical': '#4a2c5a' # Mystical border
        }
        
        self.window.configure(bg=self.colors['bg_dark'])
        
        # Center window on screen
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
        
    def create_mystical_interface(self):
        """Create the mystical voice selection interface"""
        
        # Main container with mystical styling
        main_frame = tk.Frame(
            self.window,
            bg=self.colors['bg_dark'],
            relief='raised',
            bd=3
        )
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Ornate header
        self.create_mystical_header(main_frame)
        
        # Voice selection area
        self.create_voice_selection_area(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
    def create_mystical_header(self, parent):
        """Create ornate mystical header"""
        header_frame = tk.Frame(
            parent,
            bg=self.colors['bg_medium'],
            relief='ridge',
            bd=3
        )
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with mystical styling
        title_label = tk.Label(
            header_frame,
            text="🧙‍♂️ Choose Your Mystical Voice 🧙‍♂️",
            font=('Cinzel', 18, 'bold'),
            fg=self.colors['text_gold'],
            bg=self.colors['bg_medium'],
            pady=15
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Select the voice of your AI wizard companion",
            font=('Cinzel', 11, 'italic'),
            fg=self.colors['text_light'],
            bg=self.colors['bg_medium'],
            pady=(0, 10)
        )
        subtitle_label.pack()
        
    def create_voice_selection_area(self, parent):
        """Create voice selection list and preview area"""
        selection_frame = tk.Frame(
            parent,
            bg=self.colors['bg_dark']
        )
        selection_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Voice list frame
        list_frame = tk.Frame(
            selection_frame,
            bg=self.colors['bg_medium'],
            relief='sunken',
            bd=2
        )
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # List label
        list_label = tk.Label(
            list_frame,
            text="🎭 Available Wizard Voices",
            font=('Cinzel', 12, 'bold'),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_medium'],
            pady=10
        )
        list_label.pack()
        
        # Voice listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg=self.colors['bg_medium'])
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.voice_listbox = tk.Listbox(
            listbox_frame,
            font=('Georgia', 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light'],
            selectbackground=self.colors['accent_purple'],
            selectforeground='white',
            relief='flat',
            bd=0,
            activestyle='none'
        )
        
        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical')
        self.voice_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.voice_listbox.yview)
        
        self.voice_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate voice list
        self.populate_voice_list()
        
        # Voice info panel
        self.create_voice_info_panel(selection_frame)
        
        # Bind selection event
        self.voice_listbox.bind('<<ListboxSelect>>', self.on_voice_select)
        
    def create_voice_info_panel(self, parent):
        """Create voice information and preview panel"""
        info_frame = tk.Frame(
            parent,
            bg=self.colors['bg_medium'],
            relief='raised',
            bd=2,
            width=250
        )
        info_frame.pack(side='right', fill='y')
        info_frame.pack_propagate(False)
        
        # Info label
        info_label = tk.Label(
            info_frame,
            text="🔮 Voice Details",
            font=('Cinzel', 12, 'bold'),
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_medium'],
            pady=10
        )
        info_label.pack()
        
        # Voice name
        self.voice_name_label = tk.Label(
            info_frame,
            text="Select a voice...",
            font=('Georgia', 11, 'bold'),
            fg=self.colors['text_gold'],
            bg=self.colors['bg_medium'],
            wraplength=230
        )
        self.voice_name_label.pack(pady=5)
        
        # Voice description
        self.voice_desc_label = tk.Label(
            info_frame,
            text="",
            font=('Georgia', 9),
            fg=self.colors['text_light'],
            bg=self.colors['bg_medium'],
            wraplength=230,
            justify='center'
        )
        self.voice_desc_label.pack(pady=5)
        
        # Preview button
        self.preview_button = tk.Button(
            info_frame,
            text="🎵 Preview Voice",
            font=('Cinzel', 10, 'bold'),
            fg='white',
            bg=self.colors['accent_purple'],
            activebackground=self.colors['accent_gold'],
            relief='raised',
            bd=2,
            cursor='hand2',
            command=self.preview_voice,
            state='disabled'
        )
        self.preview_button.pack(pady=15)
        
        # Status label
        self.status_label = tk.Label(
            info_frame,
            text="",
            font=('Georgia', 9, 'italic'),
            fg=self.colors['text_light'],
            bg=self.colors['bg_medium']
        )
        self.status_label.pack(pady=5)
        
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = tk.Frame(
            parent,
            bg=self.colors['bg_dark']
        )
        button_frame.pack(fill='x')
        
        # Apply button
        apply_button = tk.Button(
            button_frame,
            text="✅ Apply Selected Voice",
            font=('Cinzel', 11, 'bold'),
            fg='white',
            bg=self.colors['accent_gold'],
            activebackground='#b8941f',
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self.apply_voice,
            padx=20,
            pady=8
        )
        apply_button.pack(side='left', padx=(0, 10))
        
        # Cancel button  
        cancel_button = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Cinzel', 11, 'bold'),
            fg='white',
            bg='#666666',
            activebackground='#555555',
            relief='raised',
            bd=3,
            cursor='hand2',
            command=self.window.destroy,
            padx=20,
            pady=8
        )
        cancel_button.pack(side='right')
        
    def populate_voice_list(self):
        """Populate the voice selection list"""
        voices = WizardVoices.get_voice_list()
        current_voice = WizardVoices.CURRENT_VOICE
        
        for i, (key, name, description) in enumerate(voices):
            display_text = f"🧙‍♂️ {name}"
            self.voice_listbox.insert(tk.END, display_text)
            
            # Select current voice
            if key == current_voice:
                self.voice_listbox.selection_set(i)
                self.voice_listbox.activate(i)
                
    def on_voice_select(self, event):
        """Handle voice selection"""
        selection = self.voice_listbox.curselection()
        if selection:
            index = selection[0]
            voices = WizardVoices.get_voice_list()
            key, name, description = voices[index]
            
            # Update info display
            self.voice_name_label.config(text=f"🎭 {name}")
            self.voice_desc_label.config(text=description)
            self.preview_button.config(state='normal')
            
            # Store selected voice key
            self.selected_voice_key = key
            
    def preview_voice(self):
        """Preview the selected voice"""
        if not hasattr(self, 'selected_voice_key'):
            return
            
        self.preview_button.config(state='disabled')
        self.status_label.config(text="🎵 Generating preview...")
        
        def generate_and_play():
            try:
                # Temporarily set the voice for preview
                original_voice = WizardVoices.CURRENT_VOICE
                WizardVoices.set_voice(self.selected_voice_key)
                
                # Generate preview audio
                preview_text = "Greetings, young apprentice. I am your mystical AI companion, ready to share ancient wisdom and magical knowledge."
                duration, filepath = synthesize_audio_only(preview_text)
                
                # Play audio
                success = play_audio_system(filepath)
                
                # Restore original voice
                WizardVoices.set_voice(original_voice)
                
                # Update UI
                self.window.after(0, self._preview_complete, success, filepath)
                
            except Exception as e:
                print(f"Preview error: {e}")
                self.window.after(0, self._preview_error, str(e))
                
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=generate_and_play)
        thread.daemon = True
        thread.start()
        
    def _preview_complete(self, success, filepath):
        """Preview completion callback"""
        self.preview_button.config(state='normal')
        if success:
            self.status_label.config(text="🎵 Preview played successfully!")
        else:
            self.status_label.config(text="⚠️ Could not play preview")
        
        # Store current test audio path
        self.current_test_audio = filepath
        
        # Clear status after 3 seconds
        self.window.after(3000, lambda: self.status_label.config(text=""))
        
    def _preview_error(self, error):
        """Preview error callback"""
        self.preview_button.config(state='normal')
        self.status_label.config(text=f"❌ Preview failed: {error}")
        self.window.after(3000, lambda: self.status_label.config(text=""))
        
    def apply_voice(self):
        """Apply the selected voice"""
        if hasattr(self, 'selected_voice_key'):
            success = WizardVoices.set_voice(self.selected_voice_key)
            if success:
                voice_info = WizardVoices.get_current_voice_info()
                print(f"🧙‍♂️ Voice changed to: {voice_info['name']}")
                
                # Close window
                self.window.destroy()
                
                # Notify parent if available
                if hasattr(self.parent, 'update_voice_status'):
                    self.parent.update_voice_status(voice_info['name'])
                    
            else:
                self.status_label.config(text="❌ Failed to apply voice")
        else:
            self.status_label.config(text="⚠️ Please select a voice first")

def main():
    """Test the voice selection window"""
    root = tk.Tk()
    root.withdraw()  # Hide main window for testing
    
    app = VoiceSelectionWindow()
    app.window.mainloop()

if __name__ == "__main__":
    main()