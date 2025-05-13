# URL REQUEST OLLAMA

from groq import Groq



class apikeys:
    GROQ = "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"


client = Groq(api_key=apikeys.GROQ)

class API_URL:
    ollama_service = "http://localhost:11434/api/chat"