import math
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment


def speechToText(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("speechToText - processing")
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print("Result:" + text)

        return text


def videoToAudio(filename):
    clip = mp.VideoFileClip(filename)
    print("videoToAudio - processing")
    clip.audio.write_audiofile(filename+"_audio"+".wav")
    return


def splitAudio(filename):
    fullAudio = AudioSegment.from_wav(filename)

    total_mins = math.ceil(fullAudio.duration_seconds / 60)

    print("total mins:" + str(total_mins))

    min_per_split = 1

    def helper(from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = fullAudio[t1:t2]
        split_audio.export(split_filename, format="wav")

    for i in range(0, total_mins, min_per_split):
        split_filename = filename + "_segment_" + str(i) + ".wav"
        helper(i, i+min_per_split, split_filename)

        print(str(i) + ' Done')

        if i == total_mins - min_per_split:
            print('All splited successfully')


DIR = "./data/"

# videoToAudio(DIR+"bigVideoTest.mp4")
# speechToText(DIR+"bigVideoTest.mp4_audio.wav")
# splitAudio(DIR+"bigVideoTest.mp4_audio.wav")
