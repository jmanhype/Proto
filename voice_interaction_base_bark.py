from stt import google_stt
from llm import chatgpt
import threading
from playsound import playsound
import time

from bark import generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

class Main():
    def __init__(self) -> None:
        preload_models()  # Preload Bark models
        stt_thread = threading.Thread(target=google_stt.main, args=(self.callback_interim, self.callback_final,))
        self.llm = chatgpt.ChatGPT(valid_stream=False)
        self.latest_user_utterance = None
        self.finished_user_speeching = False

        stt_thread.start()

    def wait(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()

    def callback_interim(self, user_utterance):
        self.latest_user_utterance = user_utterance

    def callback_final(self, user_utterance):
        self.latest_user_utterance = user_utterance
        threading.Thread(target=self.main_process, args=(self.latest_user_utterance,)).start()

    def main_process(self, user_utterance):
        llm_result = self.llm.get(user_utterance)
        audio_array = generate_audio(llm_result.choices[0].message.content)
        self.audio_play(audio_array)

    def audio_play(self, audio_array):
        output_file = "tmp.wav"
        write_wav(output_file, 22050, audio_array)  # 22050 is the sample rate for Bark
        playsound(output_file)

if __name__ == '__main__':
    ins = Main()
    ins.wait()

