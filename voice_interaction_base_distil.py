from stt.distil_whisper_stt import main as distil_whisper_main
from llm import chatgpt
from tts.RealtimeTTS import RealtimeTTSWrapper
import threading
import time

class Main():
    def __init__(self) -> None:
        # Replace google_stt.main with distil_whisper_main
        stt_thread = threading.Thread(target=distil_whisper_main, args=(self.callback_interim, self.callback_final,))

        self.llm = chatgpt.ChatGPT(valid_stream=False)
        self.tts = RealtimeTTSWrapper()  # RealtimeTTS instance
        self.latest_user_utterance = None

        stt_thread.start()

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
        for thread in thread_list:  # Corrected line
            thread.join()


if __name__ == '__main__':
    ins = Main()
    ins.wait()

