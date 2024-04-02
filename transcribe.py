import sys
import os

import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from tqdm import tqdm


def extract_audio_from_video(video_path, audio_path):
    """Extracts audio from a video and saves it as a WAV file."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


import requests
import base64

def transcribe_audio(audio_path):
    # Load audio file
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Convert audio data to base64
    audio_base64bytes = base64.b64encode(audio_data)
    audio_string = audio_base64bytes.decode('utf-8')

    # Prepare the JSON payload
    data = {
        "audio": {
            "data": audio_string
        },
        "config": {
            "encoding": "LINEAR16",  # or other encoding as per your audio file
            "sampleRateHertz": 16000  # or other rate as per your audio file
        }
    }
    
    # Make the POST request
    response = requests.post('https://api.openai.com/v1/whisper/recognize', json=data)

    # Parse the response
    if response.status_code == 200:
        result = response.json()
        return result['transcript']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path to the video file as an argument.")
        sys.exit(1)

    video_path = sys.argv[1]
    audio_path = "temp_audio.wav"

    extract_audio_from_video(video_path, audio_path)
    transcription = transcribe_audio(audio_path)

    # Get the base name of the video file (without extension) and append "_transcript.txt"
    transcript_filename = os.path.splitext(os.path.basename(video_path))[
        0] + "_transcript.txt"

    if transcription:
        with open(transcript_filename, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print(f"Transcription completed! Saved to {transcript_filename}")

        # Remove the temporary audio file
        os.remove(audio_path)
    else:
        print("Transcription failed.")
