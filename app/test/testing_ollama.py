import requests

# Konfigurasi endpoint dan model
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1:8b"  # pastikan model ini sudah di-pull melalui `ollama pull llama3`

# Pesan untuk dikirim
messages = [
    {"role": "system", "content": "You are the personal assistant that help answering the question in general. answer it in 3 until 5 sentences. and act like you are talking to the user"},
    {"role": "user", "content": "Apa itu black hole?"}
]

# Kirim permintaan chat completion
response = requests.post(OLLAMA_API_URL, json={
    "model": MODEL_NAME,
    "messages": messages,
    "optional": {
                 "temperature": 0.5,
                 "repeat_penalty": 1.1,
                 "top_p": 0.8
                 },
    "stream": False  # Gunakan True jika ingin hasilnya bertahap (streaming)
})

# Tampilkan hasil
if response.status_code == 200:
    data = response.json()
    print("Jawaban:", data["message"]["content"])
else:
    print("Terjadi kesalahan:", response.text)
