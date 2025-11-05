import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        current_script_directory = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_script_directory, '.env')
        load_dotenv(dotenv_path=dotenv_path)

        self.OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "mistral:latest")
        self.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base.en")
        self.AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", 16000))
        self.AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", 1))
        raw_device_index = os.getenv("AUDIO_DEVICE_INDEX", "null")
        self.AUDIO_DEVICE_INDEX = None if raw_device_index.lower() == "null" else int(raw_device_index)
        self.VAD_AGGRESSIVENESS = int(os.getenv("VAD_AGGRESSIVENESS", 1))
        self.VAD_FRAME_MS = int(os.getenv("VAD_FRAME_MS", 30))
        self.VAD_SILENCE_TIMEOUT_S = float(os.getenv("VAD_SILENCE_TIMEOUT_S", 1.5))
        self.VAD_MIN_SPEECH_S = float(os.getenv("VAD_MIN_SPEECH_S", 0.3))
        self.VAD_MAX_RECORD_S = float(os.getenv("VAD_MAX_RECORD_S", 15))
        self.SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful and friendly conversational AI. Keep your responses concise and natural, like a human talking.")
        self.USER_NAME = os.getenv("USER_NAME", "User")
        self.AI_NAME = os.getenv("AI_NAME", "AI")
        self.TTS_RATE = int(os.getenv("TTS_RATE", 180)) # Default rate 180, adjustable via .env

cfg = Config()