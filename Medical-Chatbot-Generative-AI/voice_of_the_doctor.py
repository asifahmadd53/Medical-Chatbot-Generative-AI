# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

input_text = "Hi this is Ai with Hassan!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

# Step1b: Setup Text to Speech–TTS–model with ElevenLabs
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def text_to_speech_with_elevenlabs_old(input_text):
    audio = elevenlabs.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)
    output_filepath = "elevenlabs_output_old.mp3"
    save(audio, output_filepath)

# text_to_speech_with_elevenlabs_old(input_text) 

# Step2: Use Model for Text output to Voice
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    play_audio(output_filepath)

def play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":  # Windows
            # Use ffplay from ffmpeg package to play MP3 files
            try:
                subprocess.run(['ffplay', '-nodisp', '-autoexit', filepath], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                # If ffplay isn't available, try using the system default player
                os.startfile(filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', filepath])  # or 'aplay' for WAV files
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text):
    audio = elevenlabs.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    output_filepath = "elevenlabs_output.mp3"
    save(audio, output_filepath)
    play_audio(output_filepath)

# input_text = "Hi this is Ai with Hassan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
# text_to_speech_with_elevenlabs(input_text)