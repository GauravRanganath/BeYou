import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Video(BaseModel):
    video_name: str
    text_emotions: list
    audio_emotions: list
    video_emotions: list
    audio_seconds: int
    video_framerate: int