# URL REQUEST OLLAMA
import os
import sys
from dotenv import load_dotenv

from groq import Groq

# Load environment variables from .env file
load_dotenv()


class apikeys:
    # Uncomment and set your Groq API key here
    # GROQ = "your_groq_api_key_here"
    GROQ = os.getenv("GROQ_API_KEY")  # Get API key from environment variable

# class apikeys:
#     GROQ = ""

# Check if GROQ API key is available
if not apikeys.GROQ:
    print("ERROR: GROQ_API_KEY environment variable is not set!")
    print("Please set your Groq API key using one of these methods:")
    print("1. Export environment variable: export GROQ_API_KEY='your_api_key_here'")
    print("2. Or uncomment and set GROQ in the apikeys class in config.py")
    print("3. You can get your API key from: https://console.groq.com/keys")
    sys.exit(1)

try:
    client = Groq(api_key=apikeys.GROQ)
except Exception as e:
    print(f"ERROR: Failed to initialize Groq client: {e}")
    print("Please check your GROQ_API_KEY is valid.")
    sys.exit(1)

class API_URL:
    ollama_service = "http://localhost:11434/api/chat"

# 🧙‍♂️ Mystical Wizard Voice Configuration
class WizardVoices:
    """Configuration for different mystical wizard voices"""
    
    # Available mystical voices with descriptions
    VOICES = {
        "ancient_wizard": {
            "speaker": "p233",
            "name": "Ancient Wizard", 
            "description": "Elderly male voice - ancient wizard with mystical gravitas"
        },
        "deep_master": {
            "speaker": "p270", 
            "name": "Deep Ancient Master",
            "description": "Deep elderly voice - powerful ancient master"
        },
        "archmagus": {
            "speaker": "p282",
            "name": "Grand Archmagus", 
            "description": "Deep authoritative older voice - supreme archmagus"
        },
        "battle_sage": {
            "speaker": "p268",
            "name": "Battle-worn Sage",
            "description": "Gravelly older voice - wise battle-worn sage"
        },
        "wandering_sage": {
            "speaker": "p279",
            "name": "Wandering Sage",
            "description": "Weathered wise voice - mystical wandering sage"
        },
        "hermit_wizard": {
            "speaker": "p259",
            "name": "Hermit Wizard",
            "description": "Weathered older voice - secluded hermit wizard"
        }
    }
    
    # Default voice selection
    CURRENT_VOICE = "ancient_wizard"
    
    @classmethod
    def get_current_speaker(cls) -> str:
        """Get the current TTS speaker ID"""
        return cls.VOICES[cls.CURRENT_VOICE]["speaker"]
    
    @classmethod
    def get_current_voice_info(cls) -> dict:
        """Get current voice information"""
        return cls.VOICES[cls.CURRENT_VOICE]
    
    @classmethod 
    def set_voice(cls, voice_key: str) -> bool:
        """Set the current voice"""
        if voice_key in cls.VOICES:
            cls.CURRENT_VOICE = voice_key
            return True
        return False
    
    @classmethod
    def get_voice_list(cls) -> list:
        """Get list of available voices for UI selection"""
        return [(key, voice["name"], voice["description"]) 
                for key, voice in cls.VOICES.items()]
