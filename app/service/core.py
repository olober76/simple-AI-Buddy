from app.service.whisper_exec import transcribe



def parsing_human_input(audio_file):
    human_input = transcribe(audio_file)
    print("LOG : AI Assistant - Transcribing...")
    print(f"LOG : AI Assistant - input result: {human_input}")
    
    return human_input 