import yaml
import os
from nova.tts import TTSHandler
from nova.stt import STTHandler
from nova.commands import CommandHandler
from nova.assistant import Assistant

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    print("Initializing Nova Assistant Pro...")
    config = load_config()
    
    tts = TTSHandler(rate=config['assistant']['speech_rate'])
    stt = STTHandler()
    handler = CommandHandler(config, tts)
    
    assistant = Assistant(config, tts, stt, handler)
    
    tts.speak("Nova Assistant Pro system online.")
    assistant.run()

if __name__ == "__main__":
    main()
