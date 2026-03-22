import pyttsx3

class TTSHandler:
    def __init__(self, rate=150):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)

    def speak(self, text):
        print(f"Nova: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
