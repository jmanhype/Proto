# Import necessary libraries
import pyaudio
import queue
import threading
import time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Import other modules (assuming they are correctly implemented)
from llm import chatgpt
from tts.RealtimeTTS import RealtimeTTSWrapper

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

class DistilWhisperSTT:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = "distil-whisper/distil-large-v2"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def transcribe(self, audio_data):
        result = self.pipe(audio_data)
        return result["text"]

class Main():
    def __init__(self):
        self.stt = DistilWhisperSTT()
        self.llm = chatgpt.ChatGPT(valid_stream=False)
        self.tts = RealtimeTTSWrapper()
        self.latest_user_utterance = None

        stt_thread = threading.Thread(target=self.listen_and_transcribe)
        stt_thread.start()

    def listen_and_transcribe(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            transcript = self.stt.transcribe({"input_values": data})
            self.callback_final(transcript)

    def callback_interim(self, user_utterance):
        self.latest_user_utterance = user_utterance

    def callback_final(self, user_utterance):
        self.latest_user_utterance = user_utterance
        threading.Thread(target=self.main_process, args=(self.latest_user_utterance,)).start()

    def main_process(self, user_utterance):
        llm_result = self.llm.get(user_utterance)
        self.tts.get_audio_file_from_text(llm_result.choices[0].message.content)

    def wait(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()

if __name__ == '__main__':
    ins = Main()
    ins.wait()

