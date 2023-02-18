from speechbrain.pretrained.interfaces import foreign_class

class SpeechAnalysis(object):
    def __init__(self):
        #4 emotions: neutral (neu), happy (hap), sad (sad) and angry (ang)
        self.classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")

    def analyze(self, wav_path):
        out_prob, score, index, text_lab = self.classifier.classify_file(wav_path)
        return text_lab

if __name__=="__main__":
    speech_analyzer = SpeechAnalysis()
    print(speech_analyzer.analyze("output10.wav"))
