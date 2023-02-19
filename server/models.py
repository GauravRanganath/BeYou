import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

class Video(BaseModel):
    name: str
    epoch_date: int
    video_name: str
    text_emotions: list
    audio_emotions: list
    video_emotions: list
    audio_seconds: int
    video_framerate: int