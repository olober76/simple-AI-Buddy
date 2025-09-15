import os
import uuid
import subprocess
import sys
from TTS.api import TTS
from app.config.config import WizardVoices

try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    print("LOG : sounddevice not available, will use system audio commands")
    SOUNDDEVICE_AVAILABLE = False

TEMP_DIR = "./app/temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# 🧙‍♂️ Mystical Wizard Voice Configuration
MODEL_NAME = "tts_models/en/vctk/vits"

# Initialize TTS with mystical model
tts = TTS(MODEL_NAME)

# Ganti index sesuai hasil query_devices()
# sd.default.device =(None, 0)

def get_audio_duration(filepath: str) -> float:
    """Get audio file duration using ffprobe or sox"""
    try:
        # Try ffprobe first
        result = subprocess.run(['ffprobe', '-i', filepath, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    
    try:
        # Try sox as fallback
        result = subprocess.run(['soxi', '-D', filepath], capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    
    # Default estimate based on file size (rough approximation)
    file_size = os.path.getsize(filepath)
    return max(1.0, file_size / 32000)  # Rough estimate for 16kHz mono

def play_audio_system(filepath: str) -> bool:
    """Play audio using system commands as fallback"""
    audio_players = [
        ['paplay', filepath],           # PulseAudio
        ['aplay', filepath],            # ALSA
        ['ffplay', '-nodisp', '-autoexit', filepath],  # FFmpeg
        ['mpv', '--no-video', filepath], # MPV
        ['mplayer', filepath],          # MPlayer
    ]
    
    for player_cmd in audio_players:
        try:
            print(f"LOG : Trying to play audio with: {player_cmd[0]}")
            result = subprocess.run(player_cmd, check=True, capture_output=True)
            print(f"LOG : Audio played successfully with {player_cmd[0]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"LOG : {player_cmd[0]} failed: {e}")
            continue
    
    return False

def synthesize_audio_only(text: str) -> tuple[float, str]:
    """Generate audio file without playing it"""
    # Generate unique filename
    filename = f"{uuid.uuid4()}.wav"
    print(f"LOG : TTS - Synthesizing speech, saved in: {filename}")
    filepath = os.path.join(TEMP_DIR, filename)
    
    # Get current mystical voice
    current_speaker = WizardVoices.get_current_speaker()
    voice_info = WizardVoices.get_current_voice_info()
    print(f"LOG : Using mystical voice: {voice_info['name']} ({current_speaker})")
    
    # Synthesize speech with mystical voice
    tts.tts_to_file(text=text, speaker=current_speaker, file_path=filepath)
    
    # Get audio duration
    duration = get_audio_duration(filepath)
    
    print(f"LOG : TTS - Audio generation completed. Duration: {duration:.2f}s")
    return duration, filepath

def synthesize_and_play(text: str) -> tuple[float, str]:
    """Generate and play audio immediately (legacy function)"""
    # Generate unique filename
    filename = f"{uuid.uuid4()}.wav"
    print(f"LOG : TTS - Synthesizing speech, saved in: {filename}")
    filepath = os.path.join(TEMP_DIR, filename)
    
    # Get current mystical voice
    current_speaker = WizardVoices.get_current_speaker()
    voice_info = WizardVoices.get_current_voice_info()
    print(f"LOG : Using mystical voice: {voice_info['name']} ({current_speaker})")
    
    # Synthesize speech with mystical voice
    tts.tts_to_file(text=text, speaker=current_speaker, file_path=filepath)
    
    # Get audio duration
    duration = get_audio_duration(filepath)
    
    # Try to play audio
    audio_played = False
    
    if SOUNDDEVICE_AVAILABLE:
        try:
            # Try to find available audio devices
            devices = sd.query_devices()
            print(f"LOG : Available audio devices: {len(devices)} found")
            
            # Find a working output device
            for i, device in enumerate(devices):
                if device['max_output_channels'] > 0:
                    try:
                        print(f"LOG : Trying device {i}: {device['name']}")
                        sd.default.device = (None, i)
                        
                        # Play audio
                        data, samplerate = sf.read(filepath)
                        sd.play(data, samplerate)
                        sd.wait()
                        print(f"LOG : Audio played successfully with sounddevice on device {i}")
                        audio_played = True
                        break
                    except Exception as e:
                        print(f"LOG : Device {i} failed: {e}")
                        continue
        except Exception as e:
            print(f"LOG : sounddevice failed completely: {e}")
    
    # Fallback to system audio players
    if not audio_played:
        print("LOG : Falling back to system audio players...")
        audio_played = play_audio_system(filepath)
    
    if not audio_played:
        print("LOG : Warning - Could not play audio. Check your audio configuration.")
        print("LOG : Audio file saved at:", filepath)
    
    # Return duration for further logic
    return duration, filepath