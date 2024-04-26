# Transcriber

## Description
A tool to transcribe audio from videos using Google Speech Recognition.

## Features
- **Audio Extraction:** Extracts audio from a given video file.
- **Audio Transcription:** Transcribes the extracted audio using Google Speech Recognition.
- **Progress Indicator:** Shows progress during the transcription process.
- **Support for Multiple Formats:** Ability to process videos in various formats (depending on the capabilities of the `moviepy` library).

## Prerequisites
Ensure you have the following installed:
- Python 3.10.11
- Virtual Environment (`venv`)

To install the required Python libraries, activate your virtual environment and run:
```bash
pip install -r requirements.txt
```

## Usage
Once you've activated your virtual environment and installed the prerequisites:
```bash
python transcribe.py <path_to_video>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is open source and available under the [MIT License](LICENSE).
