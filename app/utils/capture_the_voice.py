import os
import uuid
import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

def record_with_silence_detection(on_complete=None):
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
        device_info = sd.query_devices(kind='input')
        sd.default.device = device_info['name']  # Paksa gunakan device input default

        with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, blocksize=blocksize):
            sd.sleep(int(duration_limit * 1000))
    except Exception as e:
        print("Rekaman Errors:", e)
        if on_complete:
            on_complete(None)
        return

    if recorded_audio:
        audio_data = np.concatenate(recorded_audio, axis=0)
        output_dir = "./app/temp"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.wav"
        filepath = os.path.join(output_dir, filename)

        wav_write(filepath, samplerate, audio_data)
        print(f"Audio disimpan di: {filepath}")
        if on_complete:
            on_complete(filepath)
    else:
        print("Tidak ada audio yang terekam.")
        if on_complete:
            on_complete(None)
