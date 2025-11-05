import pyttsx3
from config import cfg # For TTS_RATE

class TextToSpeech:
    def __init__(self):
        # print("TTS INFO: Initializing pyttsx3 engine (main thread)...")
        try:
            self.engine = pyttsx3.init() 
            if self.engine is None:
                raise RuntimeError("pyttsx3 engine failed to initialize (returned None).")
            # print("TTS INFO: Engine initialized.")
        except Exception as e:
            print(f"TTS FATAL: Failed to initialize pyttsx3 engine: {e}")
            raise

        try:
            self.voices = self.engine.getProperty('voices')
            if self.voices and len(self.voices) > 0:
                self.default_voice_id = self.voices[0].id 
            else:
                self.default_voice_id = None
                print("TTS WARNING: No voices found by pyttsx3.")

            # Use rate from config, defaulting to 180 if not specified
            self.engine.setProperty('rate', cfg.TTS_RATE) 
            self.engine.setProperty('volume', 1.0) # Max volume
            if self.default_voice_id:
                self.engine.setProperty('voice', self.default_voice_id)
            
            # Test speak during initialization to confirm functionality
            # print("TTS INFO: __init__ test speak starting...")
            # self.engine.say("TTS engine ready.") # Shorter test phrase
            # self.engine.runAndWait()
            # print("TTS INFO: __init__ test speak COMPLETED.")
        except Exception as e:
            print(f"TTS WARNING: Error during engine property setup or __init__ test speak: {e}")

        self._is_speaking_flag = False
        # print("TTS INFO: TextToSpeech class initialized successfully.")

    def speak(self, text, external_interrupt_event=None):
        if not text or not text.strip(): return
        if self._is_speaking_flag:
            # print("TTS WARNING: speak() called while already speaking. Attempting to stop.")
            try: self.engine.stop() 
            except: pass
            self._is_speaking_flag = False 
        self._is_speaking_flag = True
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS ERROR: Exception during blocking speak: {e}")
        finally:
            self._is_speaking_flag = False

    def is_speaking(self):
        return self._is_speaking_flag

    def stop(self):
        try:
            if self.engine: self.engine.stop()
        except Exception as e: print(f"TTS Stop: Error: {e}")
        self._is_speaking_flag = False

    def wait_until_done(self):
        # No-op for blocking speech, speak() itself waits.
        pass 