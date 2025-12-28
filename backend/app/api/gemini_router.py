# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# import asyncio
# import os
# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from google.genai import types
# from dotenv import load_dotenv
# from google import genai

# from app.services.youtube_service import get_video_transcript


# # טעינת משתני סביבה (API KEY)
# load_dotenv()
# router = APIRouter()
# client = genai.Client(api_key=os.getenv("AIR_TOUCH_KEY"), vertexai=False, http_options={'api_version': 'v1alpha',})

# MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

# tools = [
#     {
#         "function_declarations": [
#             {
#                 "name": "jump_to_video_timestamp",
#                 "description": "Navigates the video to the start of a specific topic, explanation, or mentioned segment based on semantic understanding of the user's request.",
#                 "parameters": {
#                     "type": "OBJECT",
#                     "properties": {
#                         "timestamp_seconds": {
#                             "type": "NUMBER",
#                             "description": "The exact time in seconds to jump to in the video."
#                         }
#                     },
#                     "required": ["timestamp_seconds"]
#                 }
#             }
#         ]
#     }
# ]


# @router.get("/gen-token")
# async def generate_token(video_url: str = None, current_time: int = 0):
#     try:
#         system_instruction = "You are a helpful AI assistant."

#         if video_url:
#             try:
#                 transcript = await get_video_transcript(video_url)

#                 max_words = 5000
#                 words = transcript.split()
#                 if len(words) > max_words:
#                     transcript = " ".join(words[:max_words]) + "... [Transcript truncated for brevity]"
#                 print(transcript)
#                 system_instruction = fsystem_instruction = f"""
# You are AirTouch AI, a super cute, curious, and engaging AI assistant! 🎨✨

# PERSONALITY:
# - You are friendly, warm, and have a touch of humor.
# - You are genuinely interested in what the user is watching.
# - You speak like a smart friend, not a boring robot.

# YOUR SPECIAL ABILITY:
# The user is watching a YouTube video, and you have the "secret" transcript.
# When the user asks about the video, use the transcript to be the ultimate expert! 🕵️‍♂️
# If they ask about anything else, use your amazing general knowledge.

# VIDEO TRANSCRIPT FOR CONTEXT:
# {transcript}

# GUIDELINES:
# 1. If the user asks a question about the video, answer based on the transcript but keep it interesting.
# 2. If the answer isn't in the transcript, say something like: "Hmm, the video didn't mention that, but I think..."
# 3. Keep your responses short and punchy – perfect for a conversation.
# 4. The video is currently at {current_time} seconds. Use this to understand questions about what was "just said" or "this part".

# COMMANDS & TOOL USAGE:
# - **Semantic Jump (CRITICAL)**: When the user wants to go to a specific part, use your intelligence to find the *logical start* of that topic in the transcript. Don't just look for keywords—understand the context.
# - **Trigger the Tool**: You MUST call `jump_to_video_timestamp(timestamp_seconds=NUMBER)` to actually move the video.
# - **Brief Confirmation**: Give a short, cute confirmation like "Sure thing! Jumping to the part about [Topic]..." and execute the tool immediately.
# """
#                 print(f"Token generated for video with {len(words)} words (capped at {max_words}).")
#             except Exception as e:
#                 print(f"Transcript fetch failed: {e}")

#         token = client.auth_tokens.create(
#             config={
#                 'uses': 1,
#                 'live_connect_constraints': {
#                     'model': MODEL,
#                     'config': {
#                         'system_instruction': system_instruction,
#                         'tools': tools,
#                         'session_resumption': {},
#                         'temperature': 0.7,
#                         'response_modalities': ['AUDIO']
#                     }
#                 }
#             }
#         )
#         return {"token": token.name}
#     except Exception as e:
#         print(f"Error creating token: {e}")
#         return {"error": str(e)}, 500

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio
import os
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import requests

from app.services.youtube_service import get_video_transcript

# --- Cooldown מנגנון ---
LAST_ASK_TS = 0
ASK_COOLDOWN = 10  # שניות

# טעינת משתני סביבה (API KEY)
load_dotenv()
router = APIRouter()

# === REST Gemini replacement ===
def ask_ai(prompt: str):
    # תמיכה בריבוי מפתחות API
    api_keys = []
    # קריאה מכל המפתחות שמוגדרים ב-AIR_TOUCH_KEY (ריבוי שורות/מופרדים בפסיק)
    env_keys = os.getenv("AIR_TOUCH_KEY", "")
    if "," in env_keys:
        api_keys = [k.strip() for k in env_keys.split(",") if k.strip()]
    else:
        # תמיכה בריבוי שורות בקובץ env
        api_keys = [k.strip() for k in env_keys.split("\n") if k.strip()]
    if not api_keys:
        raise Exception("לא הוגדר אף מפתח API ב-AIR_TOUCH_KEY")
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    last_exc = None
    for api_key in api_keys:
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-2.0-flash:generateContent"
            f"?key={api_key}"
        )
        try:
            response = requests.post(
                url,
                json=payload,
                verify=False,   # NetFree workaround
                timeout=30
            )
            if response.status_code == 429:
                print(f"API key {api_key} הגיע למכסה, מנסה את הבא...")
                last_exc = Exception("429 Too Many Requests")
                continue
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"שגיאה עם מפתח {api_key}: {e}")
            last_exc = e
            continue
    raise Exception(f"כל מפתחות ה-API נכשלו. שגיאה אחרונה: {last_exc}")

@router.get("/gen-token")
async def generate_token(video_url: str = None, current_time: int = 0):
    global LAST_ASK_TS
    now = time.time()
    if now - LAST_ASK_TS < ASK_COOLDOWN:
        return {
            "answer": "⏳ רגע... תני לי שנייה לחשוב 🙂"
        }
    LAST_ASK_TS = now
    try:
        system_instruction = "You are a helpful AI assistant."
        if video_url:
            try:
                transcript = await get_video_transcript(video_url)
                max_words = 5000
                words = transcript.split()
                if len(words) > max_words:
                    transcript = " ".join(words[:max_words]) + "... [Transcript truncated for brevity]"
                print(transcript)
                system_instruction = f"""
You are AirTouch AI, a super cute, curious, and engaging AI assistant! 🎨✨

PERSONALITY:
- You are friendly, warm, and have a touch of humor.
- You are genuinely interested in what the user is watching.
- You speak like a smart friend, not a boring robot.

YOUR SPECIAL ABILITY:
The user is watching a YouTube video, and you have the "secret" transcript.
When the user asks about the video, use the transcript to be the ultimate expert! 🕵️‍♂️
If they ask about anything else, use your amazing general knowledge.

VIDEO TRANSCRIPT FOR CONTEXT:
{transcript}

GUIDELINES:
1. If the user asks a question about the video, answer based on the transcript but keep it interesting.
2. If the answer isn't in the transcript, say something like: "Hmm, the video didn't mention that, but I think..."
3. Keep your responses short and punchy – perfect for a conversation.
4. The video is currently at {current_time} seconds. Use this to understand questions about what was "just said" or "this part".

COMMANDS & TOOL USAGE:
- **Semantic Jump (CRITICAL)**: When the user wants to go to a specific part, use your intelligence to find the *logical start* of that topic in the transcript. Don't just look for keywords—understand the context.
- **Trigger the Tool**: You MUST call `jump_to_video_timestamp(timestamp_seconds=NUMBER)` to actually move the video.
- **Brief Confirmation**: Give a short, cute confirmation like "Sure thing! Jumping to the part about [Topic]..." and execute the tool immediately.
"""
                print(f"Token generated for video with {len(words)} words (capped at {max_words}).")
            except Exception as e:
                print(f"Transcript fetch failed: {e}")
        answer = ask_ai(system_instruction)
        return {"answer": answer}
    except Exception as e:
        print(f"Error creating answer: {e}")
        return {"error": str(e)}, 500