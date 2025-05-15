import os
import uuid
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf

TEMP_DIR = "./app/temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# Pilih model suara orang tua (misal: vctk/vits, pilih speaker tua)
MODEL_NAME = "tts_models/en/vctk/vits"
TTS_SPEAKER = "p226"  # Ganti dengan speaker tua, misal p225 (wanita tua), p226 (pria tua), dst

tts = TTS(MODEL_NAME)

# Ganti index sesuai hasil query_devices()
sd.default.device =(None, 0)

def synthesize_and_play(text: str) -> float:
    # Generate unique filename
    filename = f"{uuid.uuid4()}.wav"

    print(f"LOG : TTS - Synthesizing speech, saved in: {filename}")
    filepath = os.path.join(TEMP_DIR, filename)
    # Synthesize speech
    tts.tts_to_file(text=text, speaker=TTS_SPEAKER, file_path=filepath)
    # Play audio
    data, samplerate = sf.read(filepath)
    sd.play(data, 48000)
    duration = len(data) / samplerate
    sd.wait()
    # Return duration for further logic
    return duration, filepath