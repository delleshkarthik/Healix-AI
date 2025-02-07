import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Step 1a: Setup Text to Speech–TTS–model with gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    # Play the audio (MP3 file)
    play_audio(output_filepath)


# Step 1b: Setup Text to Speech–TTS–model with ElevenLabs
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

    # Play the audio (MP3 file)
    play_audio(output_filepath)


# Convert MP3 to WAV for Windows compatibility
def convert_mp3_to_wav(input_filepath, output_filepath):
    audio = AudioSegment.from_mp3(input_filepath)
    audio.export(output_filepath, format="wav")
    print(f"Converted {input_filepath} to {output_filepath}")


# Play Audio (Support for macOS, Windows, Linux)
def play_audio(file_path):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', file_path])
        elif os_name == "Windows":  # Windows
            # Convert MP3 to WAV if the file is MP3 (for Windows)
            if file_path.endswith(".mp3"):
                wav_filepath = file_path.replace(".mp3", ".wav")
                convert_mp3_to_wav(file_path, wav_filepath)
                file_path = wav_filepath
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', file_path])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Test the Text to Speech functionality
input_text = "Generative-AI"

# Choose either gTTS or ElevenLabs

# Uncomment to test with gTTS
# text_to_speech_with_gtts(input_text, output_filepath="gtts_testing.mp3")

# Uncomment to test with ElevenLabs
text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing.mp3")
