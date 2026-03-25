# Proto

A voice conversation engine that chains together speech-to-text, an LLM, and text-to-speech to create a spoken dialogue loop. The user speaks, the system transcribes via Google Cloud Speech or Distil-Whisper, sends the text to GPT-3.5-turbo, and plays back the response using VoiceVox TTS.

## Status

Prototype. Last pushed November 2025. Contains compiled `.pyc` files, a Google Cloud service account JSON key (`third-harbor-175022-cd90c4fd0fd8.json`), and temporary audio files committed to the repo. No tests, no CI.

## Architecture

```
Microphone -> VAD (WebRTC) -> STT -> LLM -> TTS -> Speaker
```

| Component | Implementation | File |
|---|---|---|
| Voice Activity Detection | Google WebRTC VAD | vad/google_vad.py |
| Speech-to-Text (option 1) | Google Cloud Speech API | stt/google_stt.py |
| Speech-to-Text (option 2) | Distil-Whisper (local) | stt/distil_whisper_stt.py |
| LLM | OpenAI GPT-3.5-turbo | llm/chatgpt.py |
| Text-to-Speech | VoiceVox (local HTTP API) | tts/voicevox.py |

## Entry points

| File | STT Backend | Notes |
|---|---|---|
| voice_interaction.py | Google Cloud Speech | Main version |
| voice_interaction_base.py | Google Cloud Speech | Simplified |
| voice_interaction_base_distil.py | Distil-Whisper | Local STT |
| voice_interaction_base_bark.py | Google Cloud Speech | Bark TTS variant |
| voice_interaction_base_realtime.py | RealtimeSTT wrapper | Streaming |
| voice_interaction_llama2.py | Google Cloud Speech | Llama 2 LLM backend |
| voice_interaction_stream.py | Google Cloud Speech | Streaming variant |
| test.py | Distil-Whisper | Combined pipeline test |

## Requirements

```
openai==1.3.6
google-api-python-client==2.86.0
google-cloud-speech==2.19.0
webrtcvad==2.0.10
PyAudio==0.2.13
soundfile==0.12.1
playsound==1.3.0
```

Additional for Distil-Whisper: `torch`, `transformers`.

VoiceVox must be running locally (default: `http://localhost:50021`).

## Limitations

- A Google Cloud service account key is committed to the repo (security issue)
- `.pyc` files and `.wav` files are tracked in git
- No `.gitignore`
- Multiple entry points with overlapping functionality, no clear primary
- VoiceVox TTS requires a separate local server
- Comments are partially in Japanese

## License

None specified.