import streamlit as st
from utils import download_youtube_audio, transcribe_audio, summarize_text, text_to_speech
import os
import uuid

st.set_page_config(page_title="Sonic Sum", layout="centered")
st.title("🔊 SONIC SUMMARIZATION      ")

option = st.radio("Choose Input Type:", ["YouTube URL(s)", "Upload Audio File", "Enter Text"])
temp_dir = "downloadsss"
os.makedirs(temp_dir, exist_ok=True)

def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)

# ─── YOUTUBE ─────────────────────────────────────
if option == "YouTube URL(s)":
    urls = st.text_area("Enter YouTube URL(s) separated by commas:") or ""
    if urls.strip() and st.button("Download & Summarize"):
        for url in urls.split(","):
            url = url.strip()
            if not url:
                continue

            st.info(f"Processing: {url}")
            audio_path = download_youtube_audio(url)

            if audio_path and os.path.exists(audio_path):
                st.success(f"Downloaded: {audio_path}")
                st.audio(audio_path)

                with st.spinner("🔤 Transcribing audio..."):
                    transcript = transcribe_audio(audio_path)
                with st.spinner("🧠 Summarizing transcript..."):
                    summary = summarize_text(transcript)

                st.subheader("🎧 Transcript")
                st.text_area("Transcript", transcript, height=200)

                st.subheader("📝 Summary")
                st.write(summary)

                # TTS
                audio_summary_path = os.path.join(temp_dir, f"summary_{uuid.uuid4().hex[:8]}.mp3")
                tts_path = text_to_speech(summary, audio_summary_path)
                if tts_path and os.path.exists(tts_path):
                    st.subheader("🔊 Summary Audio")
                    st.audio(tts_path)

                cleanup_file(audio_path)
            else:
                st.error(f"Failed to download audio from: {url}")

# ─── LOCAL AUDIO ─────────────────────────────────
elif option == "Upload Audio File":
    audio_file = st.file_uploader("Upload MP3 or WAV File", type=["mp3", "wav"])
    if audio_file and st.button("Transcribe & Summarize"):
        unique_name = f"upload_{uuid.uuid4().hex[:8]}_{audio_file.name}"
        file_path = os.path.join(temp_dir, unique_name)

        with open(file_path, "wb") as f:
            f.write(audio_file.read())

        st.success(f"Uploaded file saved as: {file_path}")
        st.audio(file_path)

        with st.spinner("🔤 Transcribing audio..."):
            transcript = transcribe_audio(file_path)
        with st.spinner("🧠 Summarizing transcript..."):
            summary = summarize_text(transcript)

        st.subheader("🎧 Transcript")
        st.text_area("Transcript", transcript, height=200)

        st.subheader("📝 Summary")
        st.write(summary)

        # TTS
        audio_summary_path = os.path.join(temp_dir, f"summary_{uuid.uuid4().hex[:8]}.mp3")
        tts_path = text_to_speech(summary, audio_summary_path)
        if tts_path and os.path.exists(tts_path):
            st.subheader("🔊 Summary Audio")
            st.audio(tts_path)

        cleanup_file(file_path)

# ─── TEXT INPUT ──────────────────────────────────
elif option == "Enter Text":
    input_text = st.text_area("Enter or paste text here:")
    if input_text.strip() and st.button("Summarize & Convert to Audio"):
        with st.spinner("🧠 Summarizing text..."):
            summary = summarize_text(input_text)

        st.subheader("📝 Summary")
        st.write(summary)

        # TTS
        audio_summary_path = os.path.join(temp_dir, f"text_summary_{uuid.uuid4().hex[:8]}.mp3")
        tts_path = text_to_speech(summary, audio_summary_path)
        if tts_path and os.path.exists(tts_path):
            st.subheader("🔊 Summary Audio")
            st.audio(tts_path)
