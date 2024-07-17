import sys
import os
import logging
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from tqdm import tqdm
import time
import whisper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Create a file handler
file_handler = logging.FileHandler('transcription.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)

def extract_audio_from_video(video_path, audio_path):
    """Extracts audio from a video and saves it as a WAV file."""
    logger.info(f"Extracting audio from video: {video_path}")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    logger.info(f"Audio extracted and saved to: {audio_path}")

def transcribe_audio(audio_path, model):
    """Transcribes audio file using OpenAI Whisper."""
    audio = AudioSegment.from_wav(audio_path)
    total_length = len(audio)
    transcription = ""
    
    for i in tqdm(range(0, total_length, 30000), desc="Transcribing"):
        chunk = audio[i:i + 30000]
        chunk.export("temp_chunk.wav", format="wav")

        result = model.transcribe("temp_chunk.wav")
        transcription += result['text']

    return transcription

if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Please provide the path to the video or audio file as an argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".mp4":
        audio_path = "temp_audio.wav"
        extract_audio_from_video(file_path, audio_path)
    elif file_extension == ".wav":
        audio_path = file_path
    else:
        logger.error("Unsupported file format. Please provide an mp4 or wav file.")
        sys.exit(1)

    # Load the Whisper model
    model = whisper.load_model("base")

    print("Transcribing audio, please wait...")
    transcription = transcribe_audio(audio_path, model)

    # Get the base name of the file (without extension) and append "_transcript.txt"
    transcript_filename = os.path.splitext(os.path.basename(file_path))[0] + "_transcript.txt"

    if transcription:
        with open(transcript_filename, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print(f"Transcription completed! Saved to {transcript_filename}")
        logger.info(f"Transcription completed! Saved to {transcript_filename}")

        if file_extension == ".mp4":
            # Remove the temporary audio file only if it was created from a video
            os.remove(audio_path)
            logger.info(f"Temporary audio file removed: {audio_path}")
    else:
        print("Transcription failed.")
        logger.error("Transcription failed.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Total execution time: {elapsed_time:.2f} seconds")
    print(f"Total execution time: {elapsed_time:.2f} seconds")
