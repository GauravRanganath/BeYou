import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

class Video(BaseModel):
    name: str
    epoch_date: int
    video_name: str
    text_emotions: dict
    audio_emotions: dict
    video_emotions: dict
    audio_seconds: int
    video_framerate: int
    text_emotions_segments: list
    audio_emotions_segments: list
    video_emotions_segments: list