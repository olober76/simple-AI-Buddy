import whisper
from app.config.model import WHISPER_MODELS



model = whisper.load_model(WHISPER_MODELS.small)

def transcribe(audio_file): 
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio - must be decided
    options = whisper.DecodingOptions(language='en')
    result = whisper.decode(model, mel, options)

    # print the recognized text
    return result.text