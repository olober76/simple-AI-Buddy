from app.service.whisper_exec import transcribe
from app.utils.gui_Pop_Up_result import show_result_popup
from app.utils.gui_Loading_Wizard import show_wizard_loading
from app.service.tts_exec import synthesize_audio_only  # Changed from synthesize_and_play
import threading



def parsing_human_input(audio_file):
    human_input = transcribe(audio_file)
    print("LOG : AI Assistant - Transcribing...")
    print(f"LOG : AI Assistant - input result: {human_input}")
    
    return human_input 

# Tambahkan parameter app
def process_llama_result(result, app=None):
    if app:
        # Show loading window first
        loading_window = show_wizard_loading(app.root, 
                                           on_complete=lambda: None)  # Will be set later
        
        # Process TTS in background
        def process_audio_and_show_result():
            try:
                print("LOG : AI Assistant - Processing TTS in background...")
                duration, audio_filepath = synthesize_audio_only(result)  # Use audio_only version
                print(f"LOG : AI Assistant - TTS completed, audio saved: {audio_filepath}")
                
                # Close loading window and show result
                def show_final_result():
                    print("LOG : Closing loading window and showing result popup...")
                    loading_window.close_loading()
                    # Small delay to ensure loading window is fully closed
                    app.root.after(100, lambda: app.show_popup_and_hide_main_with_audio(result, audio_filepath))
                
                # Schedule on main thread
                app.root.after(0, show_final_result)
                
            except Exception as e:
                print(f"LOG : Error in TTS processing: {e}")
                # Still close loading and show result without audio
                def show_error_result():
                    print("LOG : Closing loading window due to TTS error...")
                    loading_window.close_loading()
                    app.root.after(100, lambda: app.show_popup_and_hide_main(result))
                
                app.root.after(0, show_error_result)
        
        # Start audio processing thread
        audio_thread = threading.Thread(target=process_audio_and_show_result, daemon=True)
        audio_thread.start()
        
    else:
        # Fallback for non-GUI usage
        show_result_popup(result)
        
    return "Success"
