from stt import google_stt
from vad import google_vad
from llm import llama2
from tts import voicevox
import threading
from playsound import playsound
import time

class Main():

    def __init__(self) -> None:
        self.valid_stream = True
        vad = google_vad.GOOGLE_WEBRTC()
        vad_thread = threading.Thread(target=vad.vad_loop, args=(self.callback_vad, ))
        stt_thread = threading.Thread(target=google_stt.main, args=(self.callback_interim, self.callback_final,))
        self.llm = llama2.Llama2(valid_stream=self.valid_stream)

        self.latest_user_utterance = None
        self.finished_user_speeching = False

        # 計測用
        self.time_user_speeching_end = None

        stt_thread.start()
        vad_thread.start()

    def wait(self):
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()

    def callback_interim(self, user_utterance):
        print("interim", user_utterance)
        self.latest_user_utterance = user_utterance

    def callback_final(self, user_utterance):
        print("final", user_utterance)
        self.latest_user_utterance = user_utterance

    def callback_vad(self, flag):
        print("vad", flag)
        if flag == True:
            self.latest_user_utterance = None
        elif self.latest_user_utterance != None:
            self.time_user_speeching_end = time.time()
            threading.Thread(target=self.main_process, args=(self.latest_user_utterance,)).start()

    def main_process(self, user_utterance):
        llm_result = self.llm.get(user_utterance)
        if self.valid_stream == False:
            # llama2のライブラリは旧バージョンのOpenAIに仕様を合わせているので微調整が必要
            agent_utterance = llm_result["choices"][0]["message"]["content"]
            wav_data, wav_length = voicevox.get_audio_file_from_text(agent_utterance)
            self.audio_play(wav_data, wav_length)
        else:
            u = ""
            for chunk in llm_result:
                # llama2のライブラリは旧バージョンのOpenAIに仕様を合わせているので微調整が必要
                if not "content" in chunk["choices"][0]["delta"]:
                    continue 
                word = chunk["choices"][0]["delta"]["content"]
                if word == None:
                    break
                u += word
                for split_word in ["、","。", "？", "！"]:
                    if split_word in u:
                        print(u)
                        wav_data, wav_length = voicevox.get_audio_file_from_text(u)
                        self.audio_play(wav_data, wav_length)
                        u = ""
            if u != "":
                wav_data, wav_length = voicevox.get_audio_file_from_text(u)
                self.audio_play(wav_data, wav_length)

    def audio_play(self, wav_data, wav_length):
        start_time = time.time()
        with open("tmp.wav", mode='bw') as f:
            f.write(wav_data)
        if self.time_user_speeching_end != None:
            print("応答までの時間", time.time() - self.time_user_speeching_end)
        self.time_user_speeching_end = None
        playsound("tmp.wav")

        while time.time() - start_time < wav_length:
            pass


if __name__ == '__main__':
    ins = Main()
    ins.wait()
