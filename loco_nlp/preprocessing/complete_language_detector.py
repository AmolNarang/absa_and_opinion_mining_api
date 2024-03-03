from loco_nlp.pipelines.super_text_cleaning import SuperCleaning
from loco_nlp.preprocessing.language_detector import detect_lang


class AllLanguageDetector:
    def __init__(self):
        self.cleaner = SuperCleaning()

    def detector(self, text):
        text = self.cleaner.super_cleaner(text)
        lang = detect_lang(text)

        return lang

    def detect_language(self, input_text):
        return list(map(self.detector, input_text)) if type(input_text) is list else self.detector(input_text)


if __name__ == "__main__":
    print("ok")
    lang_detect = AllLanguageDetector()
    print(lang_detect.detect_language('test #thisistest'))
    print(lang_detect.detect_language(['test #thisistest', 'test 2 #thisis test']))