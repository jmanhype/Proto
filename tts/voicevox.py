"""VoiceVox Text-to-Speech integration."""

import requests
import json
import time
from typing import Dict, Any, Tuple, Optional


def get_audio_query(text: str, speaker: int = 1) -> Dict[str, Any]:
    """
    Generate audio query from text using VoiceVox API.

    Args:
        text: Text to synthesize
        speaker: VoiceVox speaker ID (default: 1)

    Returns:
        Audio query data as dictionary

    Note:
        Retries indefinitely on connection errors
    """
    query_payload = {"text": text, "speaker": speaker}
    while True:
        try:
            url = "http://localhost:50021/audio_query"
            r = requests.post(url, params=query_payload, timeout=(10.0, 300.0))
            if r.status_code == 200:
                return r.json()
        except requests.exceptions.ConnectionError:
            print('fail connect...', url)
            time.sleep(0.1)


def run_synthesis(query_data: Dict[str, Any], speaker: int = 1) -> bytes:
    """
    Synthesize audio from query data using VoiceVox API.

    Args:
        query_data: Audio query dictionary from get_audio_query()
        speaker: VoiceVox speaker ID (default: 1)

    Returns:
        Audio data as bytes (WAV format)

    Note:
        Retries indefinitely on connection errors
    """
    synth_payload = {"speaker": speaker}
    while True:
        try:
            url = "http://localhost:50021/synthesis"
            r = requests.post(url, params=synth_payload, data=json.dumps(query_data), timeout=(10.0, 300.0))
            if r.status_code == 200:
                return r.content
        except requests.exceptions.ConnectionError:
            print('fail connect...', url)
            time.sleep(0.1)


def extract_wav_length(query_data: Dict[str, Any]) -> float:
    """
    Extract total audio length from query data.

    Args:
        query_data: Audio query dictionary from get_audio_query()

    Returns:
        Total audio length in seconds
    """
    length = 0.0
    for accent_phrase in query_data["accent_phrases"]:
        for mora in accent_phrase["moras"]:
            if mora["consonant_length"] is not None:
                length += mora["consonant_length"]
            if mora["vowel_length"] is not None:
                length += mora["vowel_length"]
    return length


def get_audio_file_from_text(text: str) -> Tuple[bytes, float]:
    """
    Convert text to audio using VoiceVox.

    Args:
        text: Text to synthesize

    Returns:
        Tuple of (audio_data, audio_length)
        - audio_data: WAV audio as bytes
        - audio_length: Length in seconds
    """
    query_data = get_audio_query(text)
    return run_synthesis(query_data), extract_wav_length(query_data)