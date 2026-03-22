import pvporcupine
import sounddevice as sd
import numpy as np
import time

class Assistant:
    def __init__(self, config, tts, stt, command_handler):
        self.config = config
        self.tts = tts
        self.stt = stt
        self.handler = command_handler
        self.porcupine = None
        
    def _initialize_porcupine(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.config['assistant']['access_key'],
                keyword_paths=[self.config['assistant']['wake_word_path']]
            )
            return True
        except Exception as e:
            print(f"Failed to initialize Porcupine: {e}")
            return False

    def run(self):
        if not self._initialize_porcupine():
            self.tts.speak("Error initializing wake word engine.")
            return

        print(f"Assistant {self.config['assistant']['name']} is active...")
        
        stream = sd.InputStream(
            samplerate=self.porcupine.sample_rate,
            channels=1,
            blocksize=self.porcupine.frame_length,
            dtype=np.int16
        )

        with stream:
            while True:
                try:
                    pcm, _ = stream.read(self.porcupine.frame_length)
                    pcm = pcm.flatten().astype(np.int16)
                    keyword_index = self.porcupine.process(pcm)

                    if keyword_index >= 0:
                        self.tts.speak("Yes?")
                        command = self.stt.listen()
                        if command:
                            result = self.handler.handle(command)
                            if result == "EXIT":
                                break
                        else:
                            self.tts.speak("I didn't catch that.")
                        
                        print("Waiting for wake word...")
                        
                except KeyboardInterrupt:
                    print("Assistant stopped.")
                    break
                except Exception as e:
                    print(f"Error in main loop: {e}")
                    time.sleep(1)

        if self.porcupine:
            self.porcupine.delete()
