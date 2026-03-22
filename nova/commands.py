import subprocess
import datetime
import webbrowser
import wikipedia
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class CommandHandler:
    def __init__(self, config, tts_handler):
        self.config = config
        self.tts = tts_handler
        self.apps = config.get('apps', {})
        self.search_engines = config.get('search', {})

    def _get_volume_control(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def handle(self, command):
        if not command:
            return False

        command = command.lower()

        # 1. Open Apps
        if "open" in command:
            for app_name, app_path in self.apps.items():
                if app_name in command:
                    self.tts.speak(f"Opening {app_name}")
                    subprocess.Popen(app_path, shell=True)
                    return True
            self.tts.speak("I don't know how to open that application.")
            return True

        # 2. Time
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.tts.speak(f"The current time is {now}")
            return True

        # 3. Web Search
        elif "google search" in command or "search google for" in command:
            search_query = command.replace("google search", "").replace("search google for", "").strip()
            if search_query:
                self.tts.speak(f"Searching Google for {search_query}")
                webbrowser.open(self.search_engines['google'] + search_query)
            else:
                self.tts.speak("What should I search for on Google?")
            return True

        elif "youtube search" in command or "search youtube for" in command:
            search_query = command.replace("youtube search", "").replace("search youtube for", "").strip()
            if search_query:
                self.tts.speak(f"Searching YouTube for {search_query}")
                webbrowser.open(self.search_engines['youtube'] + search_query)
            else:
                self.tts.speak("What should I search for on YouTube?")
            return True

        # 4. Wikipedia
        elif "wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            if search_query:
                try:
                    self.tts.speak(f"Searching Wikipedia for {search_query}...")
                    results = wikipedia.summary(search_query, sentences=2)
                    self.tts.speak("According to Wikipedia:")
                    self.tts.speak(results)
                except Exception as e:
                    self.tts.speak("I couldn't find anything relevant on Wikipedia.")
            else:
                self.tts.speak("What should I look up on Wikipedia?")
            return True

        # 5. System Volume
        elif "volume" in command:
            try:
                volume = self._get_volume_control()
                current_volume = volume.GetMasterVolumeLevelScalar()
                if "up" in command:
                    self.tts.speak("Increasing volume")
                    volume.SetMasterVolumeLevelScalar(min(1.0, current_volume + 0.1), None)
                elif "down" in command:
                    self.tts.speak("Decreasing volume")
                    volume.SetMasterVolumeLevelScalar(max(0.0, current_volume - 0.1), None)
                elif "mute" in command:
                    self.tts.speak("Muting audio")
                    volume.SetMute(1, None)
                elif "unmute" in command:
                    self.tts.speak("Unmuting audio")
                    volume.SetMute(0, None)
            except Exception as e:
                self.tts.speak("I had trouble adjusting the volume.")
            return True

        # 6. Exit
        elif any(word in command for word in ["stop", "exit", "goodbye"]):
            self.tts.speak("Goodbye!")
            return "EXIT"

        else:
            self.tts.speak("Command not recognized.")
            return True
        
        return False
