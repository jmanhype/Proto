import threading
import time
from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, SystemEngine
from llm import chatgpt
from vad import google_vad

class Main():
    def __init__(self):
        self.stt_recorder = AudioToTextRecorder()
        self.tts_engine = SystemEngine()
        self.tts_stream = TextToAudioStream(self.tts_engine)
        self.llm = chatgpt.ChatGPT(valid_stream=False)
        self.vad = google_vad.GOOGLE_WEBRTC()
        self.latest_user_utterance = None
        self.is_speaking = False  # Flag to check if TTS is speaking
        self.user_is_speaking = False  # Flag to check if user is speaking

        vad_thread = threading.Thread(target=self.vad.vad_loop, args=(self.callback_vad, ))
        stt_thread = threading.Thread(target=self.listen_and_transcribe)
        stt_thread.start()
        vad_thread.start()

    def listen_and_transcribe(self):
        with self.stt_recorder as recorder:
            while True:
                if not self.is_speaking and self.user_is_speaking:  # Check if user is speaking and TTS is not
                    text = recorder.text()
                    if text:
                        self.callback_final(text)

    def callback_final(self, user_utterance):
        self.latest_user_utterance = user_utterance
        threading.Thread(target=self.main_process, args=(self.latest_user_utterance,)).start()

    def callback_vad(self, flag):
        self.user_is_speaking = flag
        if not flag:
            self.latest_user_utterance = None

    def main_process(self, user_utterance):
        llm_result = self.llm.get(user_utterance)
        response_text = llm_result.choices[0].message.content
        self.speak(response_text)

    def speak(self, text):
        self.is_speaking = True
        self.tts_stream.feed(text)
        self.tts_stream.play_async()
        while self.tts_stream.is_playing():
            time.sleep(0.1)
        self.is_speaking = False

    def wait(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()

if __name__ == '__main__':
    ins = Main()
    ins.wait()

