# Proto - Voice Interaction System

A Python-based voice interaction system that combines Speech-to-Text (STT), Large Language Models (LLM), and Text-to-Speech (TTS) for natural conversational AI.

## Features

- **Multiple STT Options:**
  - Google Cloud Speech-to-Text
  - Distil-Whisper (local processing)
  - RealtimeSTT support

- **Multiple LLM Backends:**
  - OpenAI ChatGPT (GPT-3.5-turbo)
  - Llama2 (local processing via llama-cpp)

- **Multiple TTS Options:**
  - VoiceVox (Japanese TTS)
  - RealtimeTTS with Coqui engine
  - Bark TTS support

- **Voice Activity Detection (VAD):**
  - Google WebRTC VAD for detecting when users start/stop speaking

## Project Structure

```
Proto/
├── llm/                    # Language model integrations
│   ├── chatgpt.py          # OpenAI ChatGPT integration
│   └── llama2.py           # Llama2 local model integration
├── stt/                    # Speech-to-Text modules
│   ├── google_stt.py       # Google Cloud STT
│   ├── distil_whisper_stt.py  # Distil-Whisper STT
│   └── RealtimeSTT.py      # RealtimeSTT wrapper
├── tts/                    # Text-to-Speech modules
│   ├── voicevox.py         # VoiceVox TTS
│   └── RealtimeTTS.py      # RealtimeTTS wrapper
├── vad/                    # Voice Activity Detection
│   └── google_vad.py       # WebRTC VAD implementation
├── voice_interaction*.py   # Various voice interaction implementations
└── requirements.txt        # Python dependencies
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Proto
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up credentials:**
   - For Google Cloud services, set up your service account credentials
   - For OpenAI, set your API key in environment variables:
     ```bash
     export OPENAI_API_KEY=your_api_key_here
     ```

## Usage

### Basic Voice Interaction (Google STT + ChatGPT + VoiceVox)

```python
python voice_interaction.py
```

### Using Distil-Whisper STT

```python
python voice_interaction_base_distil.py
```

### Using Llama2 (Local LLM)

```python
python voice_interaction_llama2.py
```

### Real-time Streaming

```python
python voice_interaction_stream.py
```

## Configuration

### LLM Configuration

**ChatGPT:**
- Model: `gpt-3.5-turbo` (default)
- Requires OpenAI API key

**Llama2:**
- Local model path: `llm/models/elyza-q8.gguf`
- GPU layers: 50 (configurable)

### TTS Configuration

**VoiceVox:**
- Local server: `http://localhost:50021`
- Speaker ID: 1 (configurable)

### STT Configuration

**Google Cloud STT:**
- Language: Japanese (`ja-JP`)
- Sample rate: 16kHz
- Streaming recognition with interim results

## Architecture

The system follows a modular architecture:

1. **Audio Input:** Microphone captures user speech
2. **VAD:** Detects speech activity and silence
3. **STT:** Transcribes speech to text
4. **LLM:** Generates contextual responses
5. **TTS:** Converts response to speech
6. **Audio Output:** Plays synthesized speech

```
User Speech → VAD → STT → LLM → TTS → Audio Output
```

## Requirements

Core dependencies:
- `openai==1.3.6` - OpenAI API client
- `google-cloud-speech==2.19.0` - Google Cloud STT
- `webrtcvad==2.0.10` - Voice Activity Detection
- `PyAudio==0.2.13` - Audio I/O
- `playsound==1.3.0` - Audio playback

See `requirements.txt` for complete list.

## Development

### Running Tests

```bash
python test.py
```

### Code Style

This project follows Python PEP 8 style guidelines.

## Known Issues

- Temporary audio files (`.wav`) are created during TTS processing
- Google Cloud credentials must be properly configured
- VoiceVox requires a running local server

## Security Notes

⚠️ **Never commit credentials or API keys to the repository**

- Store Google Cloud credentials in a secure location
- Use environment variables for API keys
- Add credential files to `.gitignore`

## Contributing

Contributions are welcome! Please ensure:
1. Code follows existing patterns
2. No breaking changes to public APIs
3. Tests are included for new features
4. Documentation is updated

## License

[License information to be added]

## Acknowledgments

- Google Cloud Speech-to-Text
- OpenAI API
- VoiceVox TTS
- RealtimeSTT and RealtimeTTS libraries
- Llama-cpp-python
