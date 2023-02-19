from data_processing import speechToText, videoToAudio
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from text_analysis import TextAnalysis
from video_analysis import VideoAnalysis
from speech_analysis import SpeechAnalysis
import cv2
# import face_recognition
from data_processing import speechToText, videoToAudio, getTextSegments, getAudioSegmentFilenames, getFrameFilenames

app = Flask(__name__)

DIR = "./data/"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    DIR = "./data/"
    fileName = "sad2.mp4"
    text_segments = getTextSegments(DIR+fileName)
    audio_segments = getAudioSegmentFilenames(DIR+fileName)
    video_frames = getFrameFilenames(DIR+fileName)

    text_emotions = []
    for segment in text_segments:
        text_analyzer = TextAnalysis()
        # I need to get the top 3 emotions in the analysis, sorted by score
        core_emotions = text_analyzer.return_analysis(segment)[0]
        highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[:3]
        text_emotions.append(highest_emotions)

    audio_emotions = []
    for segment in audio_segments:
        speech_analyzer = SpeechAnalysis()
        audio_emotions.append(speech_analyzer.analyze(segment))

    video_emotions = []
    for frame in video_frames:
        video_analyzer = VideoAnalysis()
        core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
        highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[:3]
        video_emotions.append(highest_emotions)

    final_output = {
        "text_emotions": text_emotions,
        "audio_emotions": audio_emotions,
        "video_emotions": video_emotions
    }
    print(final_output)
    return final_output


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

@app.route("/boxes")
def draw_boxes():
    video = cv2.VideoCapture('data/happy1.mp4')

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_number = 0
    writer = cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))
    haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        try:
            ret, frame = video.read()

            frame_number += 1

            # Quit when the input video file ends
            if not ret:
                break
            if frame_number% 10 == 1:
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Loading the required haar-cascade xml classifier file


                # Applying the face detection method on the grayscale image
                faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)

            # Iterating through rectangles of detected faces
            for (x, y, w, h) in faces_rect:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Write the resulting image to the output video file
            print("Writing frame {} / {}".format(frame_number, width))
            writer.write(frame)
        except:
            print("Error writing frame {} / {}".format(frame_number, width))
            assert False

    video.release()
    writer.release()
    cv2.destroyAllWindows()



@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join("./data",'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = file.filename
    destination="/".join([target, filename])
    print(destination)
    file.save(destination)
    
    # # start processing data
    # DIR = "./data/"
    # fileName = "sad2.mp4"
    # text_segments = getTextSegments(DIR+fileName)
    # audio_segments = getAudioSegmentFilenames(DIR+fileName)
    # video_frames = getFrameFilenames(DIR+fileName)

    # text_emotions = []
    # for segment in text_segments:
    #     text_analyzer = TextAnalysis()
    #     # I need to get the top 3 emotions in the analysis, sorted by score
    #     core_emotions = text_analyzer.return_analysis(segment)[0]
    #     highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[:3]
    #     text_emotions.append(highest_emotions)

    # audio_emotions = []
    # for segment in audio_segments:
    #     speech_analyzer = SpeechAnalysis()
    #     audio_emotions.append(speech_analyzer.analyze(segment))

    # video_emotions = []
    # for frame in video_frames:
    #     video_analyzer = VideoAnalysis()
    #     core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
    #     highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[:3]
    #     video_emotions.append(highest_emotions)

    # final_output = {
    #     "text_emotions": text_emotions,
    #     "audio_emotions": audio_emotions,
    #     "video_emotions": video_emotions
    # }

    DIR = "./data/"
    fileName = "sad2.mp4"
    text_segments = getTextSegments(DIR + fileName)
    audio_segments = getAudioSegmentFilenames(DIR + fileName)
    video_frames = getFrameFilenames(DIR + fileName)

    text_emotions = []
    for segment in text_segments:
        text_analyzer = TextAnalysis()
        # I need to get the top 3 emotions in the analysis, sorted by score
        core_emotions = text_analyzer.return_analysis(segment)[0]
        highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[0]
        text_emotions.append(highest_emotions)

    audio_emotions = []
    for segment in audio_segments:
        speech_analyzer = SpeechAnalysis()
        audio_emotions.append(speech_analyzer.analyze(segment))

    video_emotions = []
    for frame in video_frames:
        video_analyzer = VideoAnalysis()
        core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
        highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[0]
        video_emotions.append(highest_emotions)

    final_output = {
        "text_emotions": text_emotions,
        "audio_emotions": audio_emotions,
        "video_emotions": video_emotions
    }
    return jsonify(final_output)

CORS(app, expose_headers='Authorization')
