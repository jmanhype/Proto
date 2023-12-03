from bark import generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# Function to preload Bark models
def preload_bark_models():
    preload_models()

# Function to generate audio from text
def get_audio_file_from_text(text):
    audio_array = generate_audio(text)
    return audio_array

# Main execution function
def main():
    # Preload models (do this once at the start)
    preload_bark_models()

    # Example text prompt
    text_prompt = "Hello, this is a test of the Bark text-to-speech system."

    # Generate audio
    audio_array = get_audio_file_from_text(text_prompt)

    # Save audio to file
    output_file = "output_audio.wav"
    write_wav(output_file, 22050, audio_array)  # 22050 is the standard sample rate for Bark

    print(f"Audio file generated and saved as {output_file}")

if __name__ == "__main__":
    main()

