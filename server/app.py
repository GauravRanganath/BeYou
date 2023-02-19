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
import math, random
from ffpyplayer.player import MediaPlayer
from moviepy.editor import *
import time

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
#
# @app.route("/test")
# def test():
#     DIR = "./data/"
#     fileName = "rama_18-february-2023.webm"
#     text_segments = getTextSegments(DIR+fileName)
#     audio_segments, audio_secs = getAudioSegmentFilenames(DIR+fileName)
#     video_frames, vid_fps = getFrameFilenames(DIR+fileName)
#
#     text_emotions = []
#     for segment in text_segments:
#         text_analyzer = TextAnalysis()
#         # I need to get the top 3 emotions in the analysis, sorted by score
#         core_emotions = text_analyzer.return_analysis(segment)[0]
#         highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[:3]
#         text_emotions.append(highest_emotions)
#
#     audio_emotions = []
#     for segment in audio_segments:
#         speech_analyzer = SpeechAnalysis()
#         audio_emotions.append(speech_analyzer.analyze(segment))
#
#     video_emotions = []
#     for frame in video_frames:
#         video_analyzer = VideoAnalysis()
#         core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
#         highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[:3]
#         video_emotions.append(highest_emotions)
#
#     final_output = {
#         "text_emotions": text_emotions,
#         "audio_emotions": audio_emotions,
#         "video_emotions": video_emotions
#     }
#     print(final_output)
#     return final_output


@app.post("/text")
def text_analyzer():
    """
    Sample output from text analyzer
    [[{'label': 'anger', 'score': 0.004419797565788031}, {'label': 'disgust', 'score': 0.0016119952779263258}, {'label': 'fear', 'score': 0.000413852947531268}, {'label': 'joy', 'score': 0.9771686792373657}, {'label': 'neutral', 'score': 0.005764602217823267}, {'label': 'sadness', 'score': 0.002092390088364482}, {'label': 'surprise', 'score': 0.008528699167072773}]]
    """
    input_string = request.form.get("input_string")
    text_analyzer = TextAnalysis()
    output_emotion = text_analyzer.return_analysis(input_string)
    text_segments = getTextSegments(DIR + fileName)
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

@app.post("/transcription")
def transcription():
    filename = request.form.get("filename")
    text_segments = getTextSegments(DIR + filename)
    return jsonify({"text_segments":text_segments})


@app.route("/boxes")
def draw_boxes():
    filename = "happy2.mp4"#request.form.filename
    DIR = "./data/"
    video = cv2.VideoCapture(DIR+filename)
    command = f"ffmpeg -y -i {DIR + filename} -ab 160k -ac 2 -ar 44100 -vn {'../client/src/pages/' + 'basicvideo.wav'}"
    subprocess.call(command, shell=True)
    fps = math.ceil(video.get(cv2.CAP_PROP_FPS))
    text_segments = getTextSegments(DIR + filename)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_number = 0
    writer = cv2.VideoWriter('../client/src/pages/'+'basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))
    haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    text_emotions = []
    text_probability = []
    for segment in text_segments:
        text_analyzer = TextAnalysis()
        # I need to get the top 3 emotions in the analysis, sorted by score
        core_emotions = text_analyzer.return_analysis(segment)[0]
        highest_emotions = sorted(core_emotions, key=lambda x: x['score'], reverse=True)[0]
        text_emotions.append(highest_emotions['label'])
        text_probability.append(highest_emotions['score'])
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
            print(frame_number%fps, frame_number, fps, int((frame_number-1)/(4*fps)), len(text_emotions))
            if frame_number% (4*fps) == 1:
                emotion_name = text_emotions[int((frame_number-1)/(4*fps))]
            prob = text_probability[int((frame_number-1)/(4*fps))]
            operator = min if prob+0.05 > 1 else max
            emotion_probability = str(f"{round(100*random.uniform(prob-0.03, operator(prob+0.03, 1)),2)}%")
            cv2.putText(frame,
                        emotion_name,
                        (150, 175),
                        font, 7,
                        (0, 255, 0),
                        2,
                        cv2.LINE_4)
            cv2.putText(frame,
                        emotion_probability,
                        (150, 325),
                        font, 3,
                        (0, 255, 0),
                        2,
                        cv2.LINE_4)
            if frame_number% 10 == 1:
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Loading the required haar-cascade xml classifier file


                # Applying the face detection method on the grayscale image
                faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)

            # Iterating through rectangles of detected faces
            for (x, y, w, h) in faces_rect:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
            # Write the resulting image to the output video file
            #print("Writing frame {} / {}".format(frame_number, width))
            writer.write(frame)
        except:
            print("Error writing frame {} / {}".format(frame_number, width))
            assert False

    video.release()
    writer.release()
    cv2.destroyAllWindows()
    return {"output_emotion":text_emotions}


def convert_webm_to_mp4(input_file, output_file):
    """
    Convert a WebM file to MP4 using FFmpeg.
    :param input_file: The path to the input WebM file.
    :param output_file: The path to the output MP4 file.
    """
    print('ffmpeg'+ '-i'+ input_file+ '-c:v'+ 'libx264'+ '-c:a'+ 'aac'+ '-strict'+ 'experimental'+ output_file)
    subprocess.call(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])

def create_emotion_count_dict(emotion_info, emotions=[]):
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

@app.route('/getData', methods=['GET'])
def getData():
    args = request.args
    name = args.get("name")
    res = []
    
    for x in video_collection.find({ "name": name }, {}):
        print("data found:", x)
        temp = {
            "name": x["name"],
            "epoch_date": x["epoch_date"],
            "video_name": x["video_name"],
            "text_emotions": x["text_emotions"],
            "audio_emotions": x["audio_emotions"],
            "video_emotions": x["video_emotions"],
            "audio_seconds": x["audio_seconds"],
            "video_framerate": x["video_framerate"],
            "text_emotions_segments": x["text_emotions_segments"],
            "audio_emotions_segments": x["audio_emotions_segments"],
            "video_emotions_segments": x["video_emotions_segments"],
            "overall_emotion": x["overall_emotion"]
        }
        res.append(temp)
        
    return jsonify(res)

@app.route('/getAverageEmotions', methods=['GET'])
def getAverageEmotions():
    args = request.args
    name = args.get("name")
    data = []
    
    for x in video_collection.find({ "name": name }, {}):
        print("data found:", x)
        temp = {
            "name": x["name"],
            "text_emotions": x["text_emotions"],
            "audio_emotions": x["audio_emotions"],
            "video_emotions": x["video_emotions"],
        }
        data.append(temp)
        
    # allEmotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Neutral', 'Sadness', 'Surprise']
    
    res = [0] * 7
    
    dataLen = len(data)
    
    # ANGER
    index = 0
    for x in data:
        res[index] += x["audio_emotions"]["angry"]
        res[index] += x["text_emotions"]["anger"]
        res[index] += x["video_emotions"]["angry"]
    res[index] = res[index] / (3 * dataLen)
    
    # Disgust
    index = 1
    for x in data:
        res[index] += x["text_emotions"]["disgust"]
        res[index] += x["video_emotions"]["disgust"]
    res[index] = res[index] / (2 * dataLen)
    
    # FEAR
    index = 2
    for x in data:
        res[index] += x["text_emotions"]["fear"]
        res[index] += x["video_emotions"]["fear"]
    res[index] = res[index] / (2 * dataLen)

    # JOY
    index = 3
    for x in data:
        res[index] += x["audio_emotions"]["happy"]
        res[index] += x["text_emotions"]["joy"]
        res[index] += x["video_emotions"]["happy"]
    res[index] = res[index] / (3 * dataLen)
    
    # NEUTRAL
    index = 4
    for x in data:
        res[index] += x["audio_emotions"]["neutral"]
        res[index] += x["text_emotions"]["neutral"]
        res[index] += x["video_emotions"]["neutral"]
    res[index] = res[index] / (3 * dataLen)
    
    # SADNESS
    index = 5
    for x in data:
        res[index] += x["audio_emotions"]["sad"]
        res[index] += x["text_emotions"]["sadness"]
        res[index] += x["video_emotions"]["sad"]
    res[index] = res[index] / (3 * dataLen)
    
    # SURPRISE
    index = 6
    for x in data:
        res[index] += x["text_emotions"]["surprise"]
        res[index] += x["video_emotions"]["surprise"]
    res[index] = res[index] / (2 * dataLen)
        
    return jsonify(res)

@app.route('/getLatestWeek', methods=['GET'])
def getLatestWeek():
    args = request.args
    name = args.get("name")
    data = []
    
    for x in video_collection.find({ "name": name }, {}):
        print("data found:", x)
        temp = {
            "name": x["name"],
            "epoch_date": int(x["epoch_date"]),
            "overall_emotion": x["overall_emotion"]
        }
        data.append(temp)
    
    # print(data)
    # dict(sorted(data.items(), key=lambda item: item["epoch_date"]))
    data.sort(key=lambda x: x["epoch_date"], reverse=True)
    # print(data)
    
    res = []
    for i in range(len(data)):
        res.append(data[i]["overall_emotion"])
    
    return jsonify(res[:7])
    
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

    text_emotion_count = create_emotion_count_dict(text_emotions, emotions=["anger","disgust","fear","joy","sadness","neutral","surprise"])
    audio_emotions = []
    for segment in audio_segments:
        emotion_dict = {"neu": "neutral", "ang": "angry", "sad": "sad", "hap": "happy", "sur": "surprise",
                        "fea": "fear", "dis": "disgust"}
        speech_analyzer = SpeechAnalysis()
        audio_emotions.append(emotion_dict[speech_analyzer.analyze(segment)[0]])

    audio_emotion_count = create_emotion_count_dict(audio_emotions, emotions=["neutral", "angry", "sad", "happy"])


    video_emotions = []
    for frame in video_frames:

        video_analyzer = VideoAnalysis()
        core_emotions = video_analyzer.analyze(frame)[0]["emotion"]
        highest_emotions = sorted(core_emotions, key=lambda x: core_emotions[x], reverse=True)[0]
        video_emotions.append(highest_emotions)

    # print("core_emotions", core_emotions)
    video_emotion_count = create_emotion_count_dict(video_emotions, emotions=core_emotions.keys())

    # allEmotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Neutral', 'Sadness', 'Surprise']
    overall_emotion = [0] * 7
    
    # ANGER
    index = 0
    overall_emotion[index] += audio_emotion_count["angry"]
    overall_emotion[index] += text_emotion_count["anger"]
    overall_emotion[index] += video_emotion_count["angry"]
    overall_emotion[index] = overall_emotion[index] / 3
    
    # Disgust
    index = 1
    overall_emotion[index] += text_emotion_count["disgust"]
    overall_emotion[index] += video_emotion_count["disgust"]
    overall_emotion[index] = overall_emotion[index] / 2
    
    # FEAR
    index = 2
    overall_emotion[index] += text_emotion_count["fear"]
    overall_emotion[index] += video_emotion_count["fear"]
    overall_emotion[index] = overall_emotion[index] / 2

    # JOY
    index = 3
    overall_emotion[index] += audio_emotion_count["happy"]
    overall_emotion[index] += text_emotion_count["joy"]
    overall_emotion[index] += video_emotion_count["happy"]
    overall_emotion[index] = overall_emotion[index] / 3
    
    # NEUTRAL
    index = 4
    overall_emotion[index] += audio_emotion_count["neutral"]
    overall_emotion[index] += text_emotion_count["neutral"]
    overall_emotion[index] += video_emotion_count["neutral"]
    overall_emotion[index] = overall_emotion[index] / 3
    
    # SADNESS
    index = 5
    overall_emotion[index] += audio_emotion_count["sad"]
    overall_emotion[index] += text_emotion_count["sadness"]
    overall_emotion[index] += video_emotion_count["sad"]
    overall_emotion[index] = overall_emotion[index] / 3
    
    # SURPRISE
    index = 6
    overall_emotion[index] += text_emotion_count["surprise"]
    overall_emotion[index] += video_emotion_count["surprise"]
    overall_emotion[index] = overall_emotion[index] / 2
    
    curr_output = {
        "name": info[0],
        "epoch_date": int(info[1]),
        "video_name": fileName,
        "text_emotions": text_emotion_count,
        "audio_emotions": audio_emotion_count,
        "video_emotions": video_emotion_count,
        "overall_emotion": overall_emotion,
        "audio_seconds": audio_secs,
        "video_framerate": math.ceil(vid_fps),
        "text_emotions_segments": text_emotions,
        "audio_emotions_segments": audio_emotions,
        "video_emotions_segments": video_emotions
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
