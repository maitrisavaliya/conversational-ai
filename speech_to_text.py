import whisper
import os
from config import cfg

class SpeechToText:
    def __init__(self):
        # print(f"STT: Loading Whisper model '{cfg.WHISPER_MODEL_SIZE}'...")
        try:
            self.model = whisper.load_model(cfg.WHISPER_MODEL_SIZE)
            # print("STT: Whisper model loaded successfully.")
        except Exception as e:
            print(f"STT: Error loading Whisper model: {e}"); raise
    def transcribe(self, audio_filepath):
        if not audio_filepath or not os.path.exists(audio_filepath): return ""
        try:
            # print(f"STT: Transcribing {os.path.basename(audio_filepath)}...")
            result = self.model.transcribe(audio_filepath, fp16=False)
            transcription = result["text"].strip()
            print(f"STT: Transcription: \"{transcription}\"") # Keep this one, it's useful
            return transcription
        except Exception as e: print(f"STT: Error transcribing: {e}"); return ""
        finally:
            if os.path.exists(audio_filepath):
                try: os.remove(audio_filepath)
                except Exception as e_del: print(f"STT: Error deleting {audio_filepath}: {e_del}")