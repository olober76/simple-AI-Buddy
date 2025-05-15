# URL REQUEST OLLAMA

from groq import Groq



class apikeys:
    GROQ = ""


client = Groq(api_key=apikeys.GROQ)

class API_URL:
    ollama_service = "http://localhost:11434/api/chat"
