import sys
import time
import queue
import pyaudio
from RealtimeSTT import AudioToTextRecorder

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

def get_current_time() -> int:
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))

def process_text(text):
    """Callback function to process the transcribed text."""
    print(GREEN + "Transcript: " + text + "\033[K")

def main():
    """Start recording and transcribe speech to text."""
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write("Transcript Results\n")
    sys.stdout.write("=====================================================\n")

    with AudioToTextRecorder() as recorder:
        # This will start recording and transcribing in real-time
        while True:
            # Fetch the transcribed text
            text = recorder.text()
            if text:
                process_text(text)

            # Check for exit condition
            if "exit" in text.lower() or "quit" in text.lower():
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                break

if __name__ == "__main__":
    main()

