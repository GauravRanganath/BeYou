from data_processing_helper import videoToAudio, splitAudio, speechToText
import os


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


def processData(filename):
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

    cleanUp(filename+"_audio"+".wav", total_secs, segmentSize)
    
    return textSegments


# DIR = "./data/"

# processData(DIR+"videoTest.mp4")
# processData(DIR+"mediumVideoTest.mp4")
# processData(DIR+"bigVideoTest.mp4")
