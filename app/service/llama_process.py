import json
import requests

from app.config.model import OLLAMA_MODELS
from app.config.config import client


def handle_transcription(transcription):
    
    print("LOG : AI Assistant - Processing on Ollama...")

    messages = [
    {"role": "system", "content": """
                                    You are the personal assistant that pretend to be a wizard in medieval era that help answering the question in general.
                                    answer it in 3 until 5 sentences. 
                                    Act like you are talking to the user because your answer will be converted as a voice.
                                    the output must be in tone like the wizard wisdom in medieval era.
                            """},
    {"role": "user", "content": f"{transcription}"}
    ]


    response = client.chat.completions.create(
        model = OLLAMA_MODELS.llama3_3_70b_versatile,
        messages = messages,
        response_format={ "type": "text" },
        temperature=0.5,
        frequency_penalty=0.6,
        top_p=0.8,
        n=1,  # Number of responses to generate at a time
        stop= None,
            
    )

    output_content = response.choices[0].message.content.strip()

        # Tampilkan hasil
    if output_content:
        print(f"LOG : AI Assistant - llama response: {output_content}")
        result = output_content
    else:
        print(f"LOG : AI Assistant - llama couldn't process your voice")
        result = "Terjadi kesalahan saat memproses suara anda, mohon coba lagi"

    return result