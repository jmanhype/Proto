# Import necessary libraries
import queue
import sys
import time
import pyaudio
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

# Terminal color schemes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

def get_current_time() -> int:
    """Return Current Time in MS."""
    return int(round(time.time() * 1000))

class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate: int, chunk_size: int) -> None:
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._fill_buffer,
        )

    def __enter__(self) -> object:
        self.closed = False
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs) -> object:
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self) -> object:
        while not self.closed:
            data = []
            if self.new_stream and self.last_audio_input:
                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)
                if chunk_time != 0:
                    if self.bridging_offset < 0:
                        self.bridging_offset = 0
                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time
                    chunks_from_ms = round((self.final_request_end_time - self.bridging_offset) / chunk_time)
                    self.bridging_offset = round((len(self.last_audio_input) - chunks_from_ms) * chunk_time)
                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])
                self.new_stream = False

            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def main(callback_interim, callback_final):
    """Start bidirectional streaming from microphone input to Distil-Whisper."""
    # Initialize Distil-Whisper model and processor
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "distil-whisper/distil-large-v2"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    # Initialize pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        torch_dtype=torch_dtype,
        device=device,
    )

    # Initialize microphone stream
    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    print(mic_manager.chunk_size)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')

    with mic_manager as stream:
        while not stream.closed:
            audio_generator = stream.generator()
            for content in audio_generator:
                if content is None:
                    break
                # Transcribe the audio chunk
                result = pipe(content)
                transcript = result["text"]
                callback_final(transcript)  # or callback_interim depending on your use case

# Define your callback functions here
def callback_interim(transcript):
    print(RED + "Interim Transcript: " + transcript + "\033[K")

def callback_final(transcript):
    print(GREEN + "Final Transcript: " + transcript + "\033[K")

if __name__ == "__main__":
    main(callback_interim, callback_final)

