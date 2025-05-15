from app.service.whisper_exec import transcribe
from app.utils.gui_Pop_Up_result import show_result_popup



def parsing_human_input(audio_file):
    human_input = transcribe(audio_file)
    print("LOG : AI Assistant - Transcribing...")
    print(f"LOG : AI Assistant - input result: {human_input}")
    
    return human_input 

# Tambahkan parameter app
def process_llama_result(result, app=None):
    if app:
        app.show_popup_and_hide_main(result)
    else:
        show_result_popup(result)
    return "Success"
