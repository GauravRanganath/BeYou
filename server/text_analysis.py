from transformers import pipeline

class TextAnalysis(object):
    def __init__(self):
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base",
                                    return_all_scores=True)
    def return_analysis(self, input_string):
        analysis_output = self.classifier(input_string)
        return analysis_output

if __name__=="__main__":
   text_analyzer = TextAnalysis()
   print(text_analyzer.return_analysis("I love this!"))