from data_processing import speechToText, videoToAudio
import os
from flask import Flask, request, session
from flask_cors import CORS, cross_origin
# from text_analysis import TextAnalysis
# from video_analysis import VideoAnalysis
# from speech_analysis import SpeechAnalysis
# import cv2
# import face_recognition
# from data_processing import speechToText, videoToAudio, getTextSegments, getAudioSegmentFilenames, getFrameFilenames

app = Flask(__name__)

DIR = "./data/"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    DIR = "./data/"
    text_segments = getTextSegments(DIR+"mediumVideoTest.mp4")
    audio_segments = getAudioSegmentFilenames(DIR+"mediumVideoTest.mp4")
    video_frames = getFrameFilenames(DIR+"mediumVideoTest.mp4")
    return text_segments

@app.post("/text")
def text_analyzer():
    """
    Sample output from text analyzer
    [[{'label': 'anger', 'score': 0.004419797565788031}, {'label': 'disgust', 'score': 0.0016119952779263258}, {'label': 'fear', 'score': 0.000413852947531268}, {'label': 'joy', 'score': 0.9771686792373657}, {'label': 'neutral', 'score': 0.005764602217823267}, {'label': 'sadness', 'score': 0.002092390088364482}, {'label': 'surprise', 'score': 0.008528699167072773}]]
    """
    input_string = request.form.get("input_string")
    text_analyzer = TextAnalysis()
    output_emotion = text_analyzer.return_analysis(input_string)
    return jsonify({"output_emotion":output_emotion})

@app.post("/image")
def image_analyzer():
    """
    Sample output from image analyzer
    [{'emotion': {'angry': 5.051945575705347e-10, 'disgust': 2.9796481272612903e-19, 'fear': 1.9366231577741707e-13, 'happy': 0.9922925224652913, 'sad': 1.9504096220575457e-09, 'surprise': 0.0004087858156530042, 'neutral': 0.007298725595918368}, 'dominant_emotion': 'happy', 'region': {'x': 319, 'y': 144, 'w': 245, 'h': 245}}]
    """
    input_image_path = request.form.get("image_path")
    video_analyzer = VideoAnalysis()
    output_emotion = video_analyzer.analyze(input_image_path)
    return jsonify({"output_emotion":output_emotion})

@app.post("/audio")
def audio_analyzer():
    """
    Sample output from audio analyzer
    ['neu']
    """
    input_audio_path = request.form.get("audio_path")
    audio_analyzer = SpeechAnalysis()
    output_emotion = audio_analyzer.analyze(input_audio_path)
    return jsonify({"output_emotion":output_emotion})

@app.post("/boxes")
def draw_boxes():
    input_video_path = request.form.get("video_path")
    cap = cv2.VideoCapture("enterfilepath.mp4")

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join("./data",'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = file.filename
    destination="/".join([target, filename])
    file.save(destination)
    
    # start processing data
    audio_segments = []
    text_segments = []
    video_frames = []
    
    # DIR = "./data/"
    # text_segments = getTextSegments(DIR+"mediumVideoTest.mp4")
    # audio_segments = getAudioSegmentFilenames(DIR+"mediumVideoTest.mp4")
    # video_frames = getFrameFilenames(DIR+"mediumVideoTest.mp4")
    
    response="Whatever you wish too return"
    return response

CORS(app, expose_headers='Authorization')
