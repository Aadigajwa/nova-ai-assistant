import speech_recognition as sr
import numpy as np
import sounddevice as sd

class STTHandler:
    def __init__(self, sample_rate=16000):
        self.recognizer = sr.Recognizer()
        self.sample_rate = sample_rate

    def listen(self, duration=5):
        print("Listening for command...")
        
        try:
            audio_array = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype="int16")
            sd.wait() 
            audio_data = audio_array.tobytes()
            audio = sr.AudioData(audio_data, self.sample_rate, 2)

            try:
                command = self.recognizer.recognize_google(audio)
                print(f"You: {command}")
                return command.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"STT Error: Could not request results; {e}")
                return None
                
        except Exception as e:
            print(f"STT Recording Error: {e}")
            return None
