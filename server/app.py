from flask import Flask, jsonify, request
from text_analysis import TextAnalysis
from video_analysis import VideoAnalysis

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<p>Hello, test!</p>"

@app.route("/test2")
def test2():
    return "<p>Hello, test2!</p>"

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


