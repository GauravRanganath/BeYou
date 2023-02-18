import speech_recognition as sr
import moviepy.editor as mp


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


# videoToAudio(DIR+"videoTest.mp4")
# speechToText(DIR+"videoTest.mp4_audio.wav")
