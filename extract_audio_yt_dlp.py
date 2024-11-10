import yt_dlp
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class YouTubeAudioTranscriber:
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        self.client = OpenAI(api_key=api_key)

    def download_audio(self, youtube_url, output_directory='audio'):
        """
        Downloads the audio from a YouTube video using yt-dlp.

        Args:
            youtube_url (str): The URL of the YouTube video.
            output_directory (str): Directory where the audio file will be saved.
        
        Returns:
            str: Path to the downloaded audio file
        """
        # Convert to absolute path
        output_directory = os.path.abspath(output_directory)
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        ydl_opts = {
            'format': 'bestaudio/best',
            'paths': {'home': output_directory},
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = ydl.prepare_filename(info)
                # Ensure we return the correct absolute path
                return os.path.join(output_directory, os.path.basename(filename))
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"Download Error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during download: {e}")

    def transcribe_audio(self, output_directory):
        """
        Transcribes the audio file using OpenAI's Whisper model.

        Args:
            audio_path (str): Path to the audio file

        Returns:
            str: Transcribed text
        """
        try:
            with open(output_directory, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            raise Exception(f"Transcription Error: {e}")

    def cleanup(self, output_directory):
        """Delete the audio file after transcription"""
        try:
            os.remove(output_directory)
            print(f"Cleaned up temporary audio file: {output_directory}")
        except Exception as e:
            print(f"Warning: Could not delete audio file {output_directory}: {e}")

    def process_video(self, youtube_url, output_directory='audio', cleanup_audio=True):
        """
        Downloads and transcribes a YouTube video.

        Args:
            youtube_url (str): YouTube video URL
            output_directory (str): Directory for audio files
            cleanup_audio (bool): Whether to delete the audio file after transcription
        
        Returns:
            str: Transcribed text
        """
        try:
            print("Downloading audio...")
            audio_path = self.download_audio(youtube_url, output_directory)
            
            if not os.path.exists(audio_path):
                raise Exception(f"Audio file not found at: {audio_path}")
            
            print(f"Audio downloaded to: {audio_path}")
            print("Transcribing audio...")
            transcript = self.transcribe_audio(audio_path)
            
            if cleanup_audio:
                self.cleanup(audio_path)
            
            return transcript
        except Exception as e:
            raise Exception(f"Processing Error: {e}")

def main():
    try:
        transcriber = YouTubeAudioTranscriber()
        
        youtube_url = input("Enter the YouTube video URL: ").strip()
        if not youtube_url:
            print("No URL provided.")
            return

        # Process the video
        transcript = transcriber.process_video(youtube_url)
        
        # Save transcript to file
        output_file = "transcript.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        # Print results
        print("\nTranscript:")
        print("-" * 50)
        print(transcript)
        print("-" * 50)
        print(f"\nTranscript saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 