import os
import yt_dlp
import whisper
from transformers import pipeline
import os
import pyttsx3

# Download audio from YouTube (no ffmpeg)
def download_youtube_audio(url):
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "yt_audio.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [],  # No ffmpeg, no conversion
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = ydl.prepare_filename(info)
            return downloaded_path

    except Exception as e:
        print(f"Error downloading from {url}: {e}")
        return None
# Transcribe using OpenAI Whisper (runs locally)
def transcribe_audio(file_path):
    try:
        print("Transcribing file:", file_path)
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        import traceback
        traceback.print_exc()  # 🔍 shows full stack trace
        return "Could not transcribe the audio."


# Summarize using Hugging Face Transformers
def summarize_text(text):
    if not text:
        return "No transcript to summarize."
    
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        summary = ""
        for chunk in chunks:
            chunk_length = len(chunk.split())
            max_len = min(100, max(20, chunk_length))  # don't go above 100, but keep min ~20
            min_len = min(25, max(5, chunk_length // 2))
            out = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
            summary += out[0]['summary_text'] + " "
        return summary.strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Could not summarize the text."

def text_to_speech(text, output_path="summary_audio.mp3"):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return output_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
