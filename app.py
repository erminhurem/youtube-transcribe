import streamlit as st
from extract_audio_yt_dlp import YouTubeAudioTranscriber
import os
from openai import OpenAI

def initialize_transcriber():
    try:
        return YouTubeAudioTranscriber()
    except ValueError as e:
        st.error(f"Error: {e}")
        st.stop()

def summarize_text(text):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please provide a concise summary of the following transcript:\n\n{text}"}
            ],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error during summarization: {str(e)}")

def main():
    st.title("YouTube Video Transcriber")
    st.write("Enter a YouTube URL to get its transcript")

    # Initialize transcriber
    transcriber = initialize_transcriber()

    # Create input field for YouTube URL
    youtube_url = st.text_input("YouTube URL")

    # Add checkboxes for options
    cleanup_audio = st.checkbox("Delete audio file after transcription", value=True)
    create_summary = st.checkbox("Generate summary using ChatGPT", value=False)

    if st.button("Transcribe"):
        if youtube_url:
            try:
                # Create a progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Update status
                status_text.text("Downloading audio...")
                progress_bar.progress(25)

                # Process the video
                transcript = transcriber.process_video(youtube_url, cleanup_audio=cleanup_audio)

                # Update progress
                progress_bar.progress(75)

                # Generate summary if requested
                summary = None
                if create_summary:
                    status_text.text("Generating summary...")
                    summary = summarize_text(transcript)

                # Update progress
                progress_bar.progress(100)
                status_text.text("Processing completed!")

                # Display results
                st.subheader("Transcript:")
                st.text_area("", transcript, height=300)

                # Add download button for transcript
                st.download_button(
                    label="Download Transcript",
                    data=transcript,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

                # Display and add download button for summary if it was generated
                if summary:
                    st.subheader("Summary:")
                    st.text_area("", summary, height=150)
                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain",
                        key="summary_download"  # Unique key to avoid conflict with transcript download
                    )

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a YouTube URL")

if __name__ == "__main__":
    main()