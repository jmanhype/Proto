from stt import google_stt
from llm import chatgpt
import threading
import time

# Import RealtimeTTS wrapper
from tts.RealtimeTTS import RealtimeTTSWrapper
  # Replace with the actual file name

class Main():
    def __init__(self) -> None:
        stt_thread = threading.Thread(target=google_stt.main, args=(self.callback_interim, self.callback_final,))
        self.llm = chatgpt.ChatGPT(valid_stream=False)
        self.tts = RealtimeTTSWrapper()  # RealtimeTTS instance
        self.latest_user_utterance = None

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
        # Directly convert text to speech using RealtimeTTS
        self.tts.get_audio_file_from_text(llm_result.choices[0].message.content)

if __name__ == '__main__':
    ins = Main()
    ins.wait()

