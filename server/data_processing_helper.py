import math
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment

r = sr.Recognizer()


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
        split_filename = filename + "_segment_" + str(i) + ".wav"
        helper(i, i+sec_per_split, split_filename)

        print(str(i) + ' Done')

        if i == total_secs - sec_per_split:
            print('All splited successfully')

    return total_secs


# DIR = "./data/"

# videoToAudio(DIR+"videoTest.mp4")
# speechToText(DIR+"bigVideoTest.mp4_audio.wav")
# splitAudio(DIR+"videoTest.mp4_audio.wav")

# videoToAudio(DIR+"bigVideoTest.mp4")
# speechToText(DIR+"bigVideoTest.mp4_audio.wav")
# splitAudio(DIR+"bigVideoTest.mp4_audio.wav")
