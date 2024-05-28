import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from transformers import pipeline

# Load environment variables
load_dotenv()

# Configure GenAI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit UI
st.title("YouTube Video Transcript Extractor And Summarize")

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return None
def generate_summary(text):
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(text, max_length=1000, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        st.error(f"Error occurred while generating summary: {str(e)}")
        return None
# Get user input for YouTube video URL
youtube_video_url = st.text_input("Enter YouTube Video URL", "")
col1,col2=st.columns(2)
# Process user input and display transcript
if col1.button("Extract Transcript"):
     
    if youtube_video_url:
        st.info("Fetching transcript... Please wait.")
        transcript = extract_transcript_details(youtube_video_url)
        if transcript:
            st.subheader("Transcript:")
            st.write(transcript)
    else:
        st.warning("Please enter a valid YouTube video URL.")
if col2.button("Generate Summary"): 
    if youtube_video_url: 
               transcript = extract_transcript_details(youtube_video_url)
               if transcript:         
                st.info("Creating summary... Please wait.")
                summary = generate_summary(transcript)
               if summary:
                st.subheader("Summary:")
                st.write(summary)
    else:
         st.warning("Unable to fetch")