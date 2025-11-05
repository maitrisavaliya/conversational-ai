import sounddevice as sd
import numpy as np
import webrtcvad
import wave
import os
import time
from collections import deque
from config import cfg

CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_AUDIO_DIR = os.path.join(CURRENT_SCRIPT_DIR, "temp_audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

class AudioHandler:
    def __init__(self):
        self.sample_rate = cfg.AUDIO_SAMPLE_RATE
        self.channels = cfg.AUDIO_CHANNELS
        self.dtype = 'int16'
        self.vad = webrtcvad.Vad(cfg.VAD_AGGRESSIVENESS)
        self.frame_duration_ms = cfg.VAD_FRAME_MS
        if self.frame_duration_ms not in [10, 20, 30]:
            self.frame_duration_ms = 30
        self.samples_per_frame = int(self.sample_rate * self.frame_duration_ms / 1000)
        self.silence_frames_needed = int(cfg.VAD_SILENCE_TIMEOUT_S * 1000 / self.frame_duration_ms)
        self.min_speech_frames = int(cfg.VAD_MIN_SPEECH_S * 1000 / self.frame_duration_ms)
        self.max_record_frames = int(cfg.VAD_MAX_RECORD_S * 1000 / self.frame_duration_ms)
        self.padding_frames = int(0.2 * 1000 / self.frame_duration_ms)
        self.padding_buffer = deque(maxlen=self.padding_frames)

        if cfg.AUDIO_DEVICE_INDEX is not None:
            try:
                sd.check_input_settings(device=cfg.AUDIO_DEVICE_INDEX, samplerate=self.sample_rate, channels=self.channels)
                # print(f"INFO: Using audio input device: {sd.query_devices(cfg.AUDIO_DEVICE_INDEX)['name']}")
            except Exception as e:
                print(f"WARNING: Error setting audio device index {cfg.AUDIO_DEVICE_INDEX}: {e}. Using default.")
                cfg.AUDIO_DEVICE_INDEX = None
        else:
            # print(f"INFO: Using default audio input device.")
            try:
                sd.check_input_settings(samplerate=self.sample_rate, channels=self.channels)
            except Exception as e:
                print(f"FATAL AudioHandler: Failed to validate audio input device: {e}")
                raise

    def record_audio_VAD(self, interrupt_event):
        recorded_audio_frames = []
        speech_detected_once = False
        silent_frames_count = 0
        active_speech_frames = 0
        total_frames_recorded_this_session = 0
        self.padding_buffer.clear()
        print(f"{cfg.USER_NAME}: Listening...")
        stream = None
        try:
            stream = sd.InputStream(
                samplerate=self.sample_rate, channels=self.channels, dtype=self.dtype,
                blocksize=self.samples_per_frame, device=cfg.AUDIO_DEVICE_INDEX
            )
            stream.start()
        except Exception as e:
            print(f"FATAL AudioHandler: Could not open/start audio input stream: {e}")
            return None
        try:
            while not interrupt_event.is_set():
                frame_data, overflowed = stream.read(self.samples_per_frame)
                if overflowed: print("WARNING: Audio input overflowed!")
                audio_segment_bytes = frame_data.tobytes()
                try: is_speech = self.vad.is_speech(audio_segment_bytes, self.sample_rate)
                except Exception: is_speech = False 
                total_frames_recorded_this_session +=1
                if is_speech:
                    if not speech_detected_once:
                        speech_detected_once = True; # print(f"{cfg.USER_NAME}: Speech detected...")
                        recorded_audio_frames.extend(list(self.padding_buffer))
                    recorded_audio_frames.append(frame_data)
                    active_speech_frames += 1; silent_frames_count = 0
                else:
                    if speech_detected_once:
                        recorded_audio_frames.append(frame_data); silent_frames_count += 1
                        if silent_frames_count >= self.silence_frames_needed: break
                    else: self.padding_buffer.append(frame_data)
                if total_frames_recorded_this_session >= self.max_record_frames:
                    # print(f"{cfg.USER_NAME}: Max recording duration reached.")
                    break
            if interrupt_event.is_set(): return None
        finally:
            if stream:
                try: stream.stop(); stream.close()
                except Exception as e_stream: print(f"WARNING: Error closing stream: {e_stream}")
        if not speech_detected_once or active_speech_frames < self.min_speech_frames: return None
        audio_data_np = np.concatenate(recorded_audio_frames)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        temp_filename = os.path.join(TEMP_AUDIO_DIR, f"rec_{timestamp}.wav")
        try:
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels); wf.setsampwidth(np.dtype(self.dtype).itemsize)
                wf.setframerate(self.sample_rate); wf.writeframes(audio_data_np.tobytes())
            return temp_filename
        except Exception as e: print(f"ERROR: Saving audio {temp_filename}: {e}"); return None