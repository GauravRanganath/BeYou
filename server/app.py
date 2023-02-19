import datetime
from data_processing import speechToText, videoToAudio
import os
import subprocess
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from text_analysis import TextAnalysis
from video_analysis import VideoAnalysis
from speech_analysis import SpeechAnalysis
import cv2
# import face_recognition
from data_processing import speechToText, videoToAudio, getTextSegments, getAudioSegmentFilenames, getFrameFilenames
from dotenv import dotenv_values
from pymongo import MongoClient
from models import Video
import math

app = Flask(__name__)

DIR = "./data/"
config = dotenv_values("env")

app.mongodb_client = MongoClient(config["ATLAS_URI"])
app.database = app.mongodb_client[config["DB_NAME"]]
video_collection = app.database["video_collection"]
print("Connected to the MongoDB database!")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    DIR = "./data/"
    fileName = "rama_18-february-2023.webm"
    text_segments = getTextSegments(DIR+fileName)
    audio_segments, audio_secs = getAudioSegmentFilenames(DIR+fileName)
    video_frames, vid_fps = getFrameFilenames(DIR+fileName)

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
    fps = video.get(cv2.CAP_PROP_FPS)
    print(fps)
    assert(0)
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
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Use putText() method for
            # inserting text on video
            cv2.putText(frame,
                        'TEXT ON VIDEO',
                        (50, 50),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            if frame_number% 10 == 1:
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Loading the required haar-cascade xml classifier file


                # Applying the face detection method on the grayscale image
                faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)

            # Iterating through rectangles of detected faces
            for (x, y, w, h) in faces_rect:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            # Write the resulting image to the output video file
            print("Writing frame {} / {}".format(frame_number, width))
            writer.write(frame)
        except:
            print("Error writing frame {} / {}".format(frame_number, width))
            assert False

    video.release()
    writer.release()
    cv2.destroyAllWindows()


def convert_webm_to_mp4(input_file, output_file):
    """
    Convert a WebM file to MP4 using FFmpeg.
    :param input_file: The path to the input WebM file.
    :param output_file: The path to the output MP4 file.
    """
    print('ffmpeg'+ '-i'+ input_file+ '-c:v'+ 'libx264'+ '-c:a'+ 'aac'+ '-strict'+ 'experimental'+ output_file)
    subprocess.call(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])

def create_emotion_count_dict(emotion_info):
    emotions = ["neutral", "angry", "sad", "happy", "surprise", "fear", "disgust"]
    # create count dictionary with each emotion
    emotion_count = {emotion: 0 for emotion in emotions}
    # iterate through each emotion in the text emotions
    for emotion in emotion_info:
        # increment the count for that emotion
        emotion_count[emotion] += 1
    # divide each emotion count by the total number of emotions
    emotion_count = {emotion: 100*emotion_count[emotion] / len(emotion_info) for emotion in emotions}
    return emotion_count

def extractInfoFromName(filename):
    arr = filename.split('.')
    arr = arr[0].split('_')
    print("info:", arr)
    return arr

@app.route('/upload', methods=['POST'])
def fileUpload():
    # save file
    DIR = "./data/"
    
    target=os.path.join(DIR)
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = file.filename
    destination="/".join([target, filename])
    print(destination)
    file.save(destination)
    
    # convert to mp4
    fileName = file.filename
    
    convert_webm_to_mp4(DIR + fileName, DIR + fileName + ".mp4")
    
    fileName = fileName + ".mp4"
    
    info = extractInfoFromName(fileName)
    
    text_segments = getTextSegments(DIR + fileName)
    audio_segments, audio_secs = getAudioSegmentFilenames(DIR + fileName)
    video_frames, vid_fps = getFrameFilenames(DIR + fileName)

    text_emotions = []
    for segment in text_segments:
        text_analyzer = TextAnalysis()
        # I need to get the top 3 emotions in the analysis, sorted by score
        core_emotions = text_analyzer.return_analysis(segment)[0]
        highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[0]
        text_emotions.append(highest_emotions['label'])

    text_emotion_count = create_emotion_count_dict(text_emotions)
    audio_emotions = []
    for segment in audio_segments:
        emotion_dict = {"neu": "neutral", "ang": "angry", "sad": "sad", "hap": "happy", "sur": "surprised",
                        "fea": "fear", "dis": "disgust"}
        speech_analyzer = SpeechAnalysis()
        audio_emotions.append(emotion_dict[speech_analyzer.analyze(segment)[0]])

    audio_emotion_count = create_emotion_count_dict(audio_emotions)


    video_emotions = []
    for frame in video_frames:

        video_analyzer = VideoAnalysis()
        core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
        highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[0]
        video_emotions.append(highest_emotions)

    video_emotion_count = create_emotion_count_dict(video_emotions)

    curr_output = {
        "name": info[0],
        "epoch_date": int(info[1]),
        "video_name": fileName,
        "text_emotions": text_emotion_count,
        "audio_emotions": audio_emotion_count,
        "video_emotions": video_emotion_count,
        "audio_seconds": audio_secs,
        "video_framerate": math.ceil(vid_fps),
    }
    final_output = curr_output.copy()
    analysis_output = Video(**final_output)
    video_collection.insert_one(analysis_output.__dict__)
    existing_row = video_collection.find_one({"video_name": final_output["video_name"]})

    # If a document with the same filename exists, update its content
    if existing_row:
        video_collection.update_one({"video_name": existing_row["video_name"]}, {"$set": existing_row})
    else:
        # Otherwise, insert a new document with the given row
        video_collection.insert_one(final_output)
    return jsonify(final_output)

CORS(app, expose_headers='Authorization')
