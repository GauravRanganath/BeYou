from deepface import DeepFace

class VideoAnalysis(object):
    def __init__(self):
        self.actions = ("emotion")

    def analyze(self, img_path):
        objs = DeepFace.analyze(img_path=img_path, actions=self.actions, enforce_detection=False)
        for emotion in objs[0]['emotion']:
            objs[0]['emotion'][emotion] = objs[0]['emotion'][emotion]/100
        return objs

if __name__=="__main__":
    video_analyzer = VideoAnalysis()
    print(video_analyzer.analyze("happy_face.png"))