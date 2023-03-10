import math
from data_processing_helper import videoToAudio, splitAudio, speechToText, extractFrames
import os
from pydub import AudioSegment
import glob
import speech_recognition as sr


def buildTextSegments(filename, total_secs, sec_per_split):
    res = []
    for i in range(0, total_secs, sec_per_split):
        try:
            temp = speechToText(filename+"_segment_"+str(math.ceil(i/sec_per_split))+".wav")
            res.append(temp)
        except sr.UnknownValueError:
            res.append("unknown")
    return res


def cleanUp(filename, total_secs, sec_per_split):
    # print("remove audio")
    os.remove(filename)

    # print("remove segments")
    for i in range(0, total_secs, sec_per_split):
        os.remove(filename+"_segment_"+math.ceil(i/sec_per_split)+".wav")


def getTextSegments(filename):
    # convert video to audio
    videoToAudio(filename)

    # split audio
    segmentSize = 4
    total_secs = splitAudio(filename+"_audio"+".wav", segmentSize)

    # build text segments
    textSegments = buildTextSegments(
        filename+"_audio"+".wav", total_secs, segmentSize)

    print()
    for i in range(len(textSegments)):
        print(str(i) + " - " + textSegments[i])

    # cleanUp(filename+"_audio"+".wav", total_secs, segmentSize)
    
    return textSegments


def getAudioSegmentFilenames(filename):
    filename = filename+"_audio"+".wav"
    fullAudio = AudioSegment.from_wav(filename)
    total_secs = math.ceil(fullAudio.duration_seconds)
    segmentSize = 4
    
    res = []
    for i in range(0, total_secs, segmentSize):
        res.append(filename+"_segment_"+str(math.ceil(i/segmentSize))+".wav")
    return res, total_secs


def getFrameFilenames(filename):
    return extractFrames(filename)
    
  
DIR = "./data/"

# print(getFrameFilenames(DIR+"mediumVideoTest.mp4"))

# DIR = "./data/"
# getTextSegments(DIR+"mediumVideoTest.mp4")
# print(getAudioSegmentFilenames(DIR+"mediumVideoTest.mp4"))

# getTextSegments(DIR+"videoTest.mp4")
# getTextSegments(DIR+"mediumVideoTest.mp4")
# getTextSegments(DIR+"bigVideoTest.mp4")
