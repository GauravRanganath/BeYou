import math
from data_processing_helper import videoToAudio, splitAudio, speechToText
import os
from pydub import AudioSegment


def buildTextSegments(filename, total_secs, sec_per_split):
    res = []
    for i in range(0, total_secs, sec_per_split):
        temp = speechToText(filename+"_segment_"+str(i)+".wav")
        res.append(temp)
    return res


def cleanUp(filename, total_secs, sec_per_split):
    # print("remove audio")
    os.remove(filename)

    # print("remove segments")
    for i in range(0, total_secs, sec_per_split):
        os.remove(filename+"_segment_"+str(i)+".wav")


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
        res.append(filename+"_segment_"+str(i)+".wav")
    return res

# DIR = "./data/"
# getTextSegments(DIR+"mediumVideoTest.mp4")
# print(getAudioSegmentFilenames(DIR+"mediumVideoTest.mp4"))

# getTextSegments(DIR+"videoTest.mp4")
# getTextSegments(DIR+"mediumVideoTest.mp4")
# getTextSegments(DIR+"bigVideoTest.mp4")
