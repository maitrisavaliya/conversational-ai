import threading
import time
import os
from config import cfg
from audio_handler import AudioHandler
from speech_to_text import SpeechToText
from llm_handler import LLMHandler
from text_to_speech import TextToSpeech

# This flag is less effective for TTS if TTS is blocking, but kept for general structure
tts_general_interrupt_flag = threading.Event() 
audio_recording_interrupt_flag = threading.Event()

EXIT_COMMANDS = ["goodbye", "exit", "quit", "bye", "bye bye", "that's all"]
CLEAR_HISTORY_COMMANDS = ["clear history", "reset conversation", "forget everything", "start over"]

def main_conversation_loop():
    print("Initializing components...")
    try:
        audio = AudioHandler(); stt = SpeechToText()
        llm = LLMHandler(); tts = TextToSpeech()
    except Exception as e:
        print(f"FATAL: Could not initialize components: {e}"); import traceback; traceback.print_exc(); return

    print(f"\n--- {cfg.AI_NAME} is ready ---")
    print(f"Say '{'/'.join(EXIT_COMMANDS)}' to end the conversation.")
    # print(f"System Prompt (for AI): {cfg.SYSTEM_PROMPT}") # For dev reference if needed
    print("-------------------------\n")
    
    initial_greeting = f"Hello! I'm {cfg.AI_NAME}. How can I help you today?"
    print(f"{cfg.AI_NAME}: {initial_greeting}")
    tts.speak(initial_greeting) # Will block until done

    try:
        while True:
            audio_recording_interrupt_flag.clear(); tts_general_interrupt_flag.clear()
            
            temp_audio_file = audio.record_audio_VAD(audio_recording_interrupt_flag) 

            if audio_recording_interrupt_flag.is_set(): continue
            
            # Interruption logic for TTS is mostly moot if TTS is blocking
            # if tts.is_speaking(): # This should be false after blocking speak
            #     print(f"MainLoop: User interrupted. Stopping TTS.") # Unlikely to hit
            #     tts.stop(); 
            
            if not temp_audio_file: time.sleep(0.1); continue
            
            user_text = stt.transcribe(temp_audio_file) # STT prints transcription

            if not user_text:
                msg = "I didn't quite catch that. Could you please try again?"
                print(f"{cfg.AI_NAME}: {msg}")
                tts.speak(msg); continue
            
            if user_text.lower().strip() in EXIT_COMMANDS:
                msg = "Goodbye! It was nice talking to you."
                print(f"{cfg.AI_NAME}: {msg}")
                tts.speak(msg); break
            
            if user_text.lower().strip() in CLEAR_HISTORY_COMMANDS:
                llm.clear_history()
                msg = "Okay, I've cleared our conversation history. Let's start fresh!"
                print(f"{cfg.AI_NAME}: {msg}"); tts.speak(msg); continue
            
            ai_response_text = llm.get_response(user_text) # LLM handler prints its streaming output

            if ai_response_text:
                tts.speak(ai_response_text) # Blocks until done
            else:
                msg = "I don't have a response for that right now."
                print(f"{cfg.AI_NAME}: {msg}")
                tts.speak(msg)
            
    except KeyboardInterrupt: print("\nProgram interrupted by user (Ctrl+C).")
    except Exception as e: print(f"\nMainLoop: An unexpected error occurred: {e}"); import traceback; traceback.print_exc()
    finally:
        print("Cleaning up and exiting...")
        audio_recording_interrupt_flag.set() # Signal audio recording to stop if active
        # if 'tts' in locals() and tts.is_speaking(): tts.stop() # Less critical with blocking
        
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_audio")
        if os.path.exists(temp_dir):
            for f_name in os.listdir(temp_dir):
                if f_name.endswith(".wav") and f_name.startswith("rec_"): 
                    try: os.remove(os.path.join(temp_dir, f_name))
                    except Exception as e_del: print(f"Error deleting temp file {f_name}: {e_del}")
        print(f"--- {cfg.AI_NAME} session ended. ---")

if __name__ == "__main__":
    main_conversation_loop()