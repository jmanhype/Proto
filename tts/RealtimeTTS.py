# Import necessary libraries
from RealtimeTTS import TextToAudioStream, CoquiEngine
import time

class RealtimeTTSWrapper:
    def __init__(self):
        # Initialize the Coqui TTS engine
        # You may need to specify the path to the model if you've downloaded it
        self.engine = CoquiEngine()  
        self.stream = TextToAudioStream(self.engine)

    def get_audio_file_from_text(self, text):
        self.stream.feed(text)
        self.stream.play_async()
        # Wait until the audio has finished playing
        while self.stream.is_playing():
            time.sleep(0.1)

# Example usage
if __name__ == "__main__":
    tts = RealtimeTTSWrapper()
    tts.get_audio_file_from_text("Hello world! How are you today?")

