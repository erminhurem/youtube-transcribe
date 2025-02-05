# YouTube Video Transcriber

A Streamlit web application that transcribes YouTube videos using OpenAI's Whisper model. The application downloads the audio from YouTube videos and converts speech to text, providing accurate transcriptions.

## Features

- Easy-to-use web interface built with Streamlit
- YouTube video audio extraction using yt-dlp
- High-quality transcription using OpenAI's Whisper model
- Option to automatically clean up audio files after transcription
- Progress tracking during the transcription process

## Prerequisites

- Python 3.6 or higher
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/youtube-video-transcriber.git
cd youtube-video-transcriber
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter a YouTube URL in the input field

4. Choose whether to delete the audio file after transcription (recommended to save space)

5. Click "Transcribe" and wait for the process to complete

## Project Structure

- `app.py`: Main Streamlit web application
- `extract_audio_yt_dlp.py`: YouTube audio extraction and transcription logic
- `requirements.txt`: Project dependencies
- `.env`: Environment variables configuration

## Dependencies

- yt-dlp: For YouTube video downloading
- openai: For accessing the Whisper transcription API
- python-dotenv: For environment variable management
- streamlit: For the web interface

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper transcription model
- yt-dlp for YouTube video downloading capabilities
- Streamlit for the web application framework 
