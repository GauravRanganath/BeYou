from data_processing import speechToText, videoToAudio
from flask import Flask

app = Flask(__name__)

DIR = "./data/"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test")
def test():
    videoToAudio(DIR+"videoTest.mp4")
    text = speechToText(DIR+"videoTest.mp4_audio.wav")
    return text
