import io
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


def transcribe_audio(audio_path):
    """Transcribes the given audio file using Google Speech Recognition."""
    r = sr.Recognizer()

    # Split the audio into 30-second segments
    segment_duration = 30  # in seconds
    audio = AudioSegment.from_wav(audio_path)
    duration = len(audio) / 1000  # Total duration in seconds
    segments = int(duration / segment_duration)

    transcription = ""

    for i in tqdm(range(segments + 1), desc="Transcribing", unit="segment"):
        start_time = i * segment_duration * 1000
        end_time = (i + 1) * segment_duration * 1000
        audio_segment = audio[start_time:end_time]

        # Save the audio segment to a temporary file
        temp_filename = f"temp_segment_{i}.wav"
        audio_segment.export(temp_filename, format="wav")

        with sr.AudioFile(temp_filename) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data, language='pt-BR')
                transcription += text + " "
            except sr.UnknownValueError:
                print(f"Segment {i + 1} not recognized.")
            except sr.RequestError as e:
                print(f"API request error on segment {i + 1}.")
                break  # Stop if there's an error calling the API

        # Remove the temporary file after using it
        os.remove(temp_filename)

    return transcription.strip()


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
