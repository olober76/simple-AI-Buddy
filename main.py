import tkinter as tk
from app.utils.gui_Service import AIAssistantApp
from app.service.llama_process import handle_transcription
from app.service.core import process_llama_result


if __name__ == "__main__":
    print("LOG : AI Assistant - Starting...")
    root = tk.Tk()
    app = AIAssistantApp(root)
    
    # Set up the callback dengan wrapper function
    app.set_transcription_callback(lambda x: process_llama_result(handle_transcription(x)))
    
    root.mainloop()
