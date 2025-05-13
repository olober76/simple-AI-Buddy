import tkinter as tk
from app.utils.gui_Service import AIAssistantApp
from app.service.ollama_process import handle_transcription



if __name__ == "__main__":
    print("LOG : AI Assistant - Starting...")
    root = tk.Tk()
    app = AIAssistantApp(root)
    ollama_result = app.set_transcription_callback(handle_transcription)
    root.mainloop()
