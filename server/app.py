from data_processing import speechToText, videoToAudio
import os
from flask import Flask, request, session
from flask_cors import CORS, cross_origin


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

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join("./data",'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = file.filename
    destination="/".join([target, filename])
    file.save(destination)
    response="Whatever you wish too return"
    return response

CORS(app, expose_headers='Authorization')
