import os
os.environ["REQUESTS_CA_BUNDLE"] = r"C:\\ProgramData\\NetFree\\CA\\netfree-ca-bundle-curl.crt"
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fastapi import HTTPException
from typing import List, Dict, Any
import os

TRANSCRIPT_CACHE: Dict[str, str] = {}

def extract_video_id(url: str) -> str:
    """
    מחלץ את ה-ID של הסרטון מתוך ה-URL.
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

async def get_video_transcript(video_url: str)-> str:
    """
    מקבל URL, שולף את התמלול באופן אוטומטי ומחזיר אותו כמחרוזת אחת באיזשהי שפה שנמצאה.
    """
    transcript = ""
    try:
        video_id = extract_video_id(video_url)
        if video_id in TRANSCRIPT_CACHE:
            print(f"Returning cached transcript for video_id: {video_id}")
            return TRANSCRIPT_CACHE[video_id]
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        try:
            transcript_to_fetch = transcript_list.find_transcript(['he', 'en'])
        except NoTranscriptFound:
            all_transcripts = list(transcript_list)
            if not all_transcripts:
                print("No direct or translatable transcript found for this video in available languages.")
                return ""
            transcript_to_fetch = all_transcripts[0]
            print(f"Warning: Using transcript in {transcript_to_fetch.language} - Gemini will translate.")
        raw_data = transcript_to_fetch.fetch().to_raw_data()
        formatted_segments = []
        for item in raw_data:
            start_time = int(item['start'])
            text = item['text'].replace("\n", " ")
            formatted_segments.append(f"[{start_time}s] {text}")
        full_text_with_timestamps = " ".join(formatted_segments)
        result = f"[LANGUAGE_CODE: {transcript_to_fetch.language_code}] {full_text_with_timestamps}"
        TRANSCRIPT_CACHE[video_id] = result
        transcript = result
    except TranscriptsDisabled:
        print("Transcript is disabled for this video by the creator.")
        transcript = ""
    except NoTranscriptFound:
        print("No direct or translatable transcript found for this video in available languages.")
        transcript = ""
    except Exception as e:
        print(f"Transcript fetch failed: {e}")
        transcript = ""
    return transcript