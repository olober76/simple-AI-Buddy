from app.service.whisper_exec import transcribe
from app.utils.gui_Pop_Up_result import show_result_popup



def parsing_human_input(audio_file):
    human_input = transcribe(audio_file)
    print("LOG : AI Assistant - Transcribing...")
    print(f"LOG : AI Assistant - input result: {human_input}")
    
    return human_input 

def process_llama_result(result):
    # Show the result in a popup window
    show_result_popup(result)
    return "Success"
