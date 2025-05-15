import tkinter as tk
from app.utils.gui_Service import AIAssistantApp
from app.service.llama_process import handle_transcription
from app.service.core import process_llama_result


if __name__ == "__main__":
    print("LOG : AI Assistant - Starting...")
    root = tk.Tk()
    app = AIAssistantApp(root)
    
    # Pass app ke process_llama_result
    app.set_transcription_callback(lambda x: process_llama_result(handle_transcription(x), app=app))
    
    root.mainloop()
