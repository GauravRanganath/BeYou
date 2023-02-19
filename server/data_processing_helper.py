import math
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import cv2
import math

r = sr.Recognizer()


def extractFrames(filename):
    print()
    print("extractFrames - processing: " + filename)
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    count = 0

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print('frames per second =', fps)

    limit = math.ceil(fps)
    
    res = []

    while success:
        if (count % limit == 0):
            temp = filename+"_frame"+str(math.ceil(count/limit))+".jpg"
            print(temp)
            res.append(temp)
            cv2.imwrite(temp, image)
        success, image = vidcap.read()
        count += 1
        
    return res, fps


def speechToText(filename):
    print()
    with sr.AudioFile(filename) as source:
        print("speechToText - processing: " + filename)
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        # print("Result:" + text)

        return text


def videoToAudio(filename):
    print()
    clip = mp.VideoFileClip(filename)
    print("videoToAudio - processing: " + filename)
    clip.audio.write_audiofile(filename+"_audio"+".wav")
    return


def splitAudio(filename, segmentSize):
    print()
    print("splitAudio - processing: " + filename)

    fullAudio = AudioSegment.from_wav(filename)

    total_secs = math.ceil(fullAudio.duration_seconds)

    print("total_secs:" + str(total_secs))

    sec_per_split = segmentSize

    def helper(from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        split_audio = fullAudio[t1:t2]
        split_audio.export(split_filename, format="wav")

    for i in range(0, total_secs, sec_per_split):
        split_filename = filename + "_segment_" + str(math.ceil(i/sec_per_split)) + ".wav"
        helper(i, i+sec_per_split, split_filename)

        print(str(i) + split_filename + ' Done')

        if i == total_secs - sec_per_split:
            print('All splited successfully')

    return total_secs


DIR = "./data/"
# extractFrames(DIR+"bigVideoTest.mp4")
# extractFrames(DIR+"mediumVideoTest.mp4")

# videoToAudio(DIR+"videoTest.mp4")
# speechToText(DIR+"bigVideoTest.mp4_audio.wav")
# splitAudio(DIR+"videoTest.mp4_audio.wav")

# videoToAudio(DIR+"bigVideoTest.mp4")
# speechToText(DIR+"bigVideoTest.mp4_audio.wav")
# splitAudio(DIR+"bigVideoTest.mp4_audio.wav")
