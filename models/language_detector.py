from pycld2 import detect
from polyglot.detect import Detector
from loco_nlp.preprocessing.hinglish_detector import HinglishDetector

hd = HinglishDetector()


def detect_lang(text):
    try:
        lang = detect(text)[2][0][1]
        lang = lang.split("-")[0]
        if lang not in ["un"]:
            return lang
    except Exception as e:
        print("Error with language detection:", e)

    try:
        lang = Detector(text).language.code
        lang = lang.split("_")[0]
        return lang
    except Exception as e:
        print("Error with language detection :", e)

    return None


def pure_en_detector(text):
    if detect_lang(text) == 'en':
        if hd.detect(text):
            return 'en_hi'
        else:
            return 'en'
    return detect_lang(text)


def detect_lang_list(text_list):
    lang_list = list(map(detect_lang, text_list))
    return lang_list


if __name__ == "__main__":
    from time import time

    x = time()
    # for i in range(1):
    #     import string
    #     line = """So nice👍 #jewelchangiairport #singapore #สิงคโปร์ใครก็เที่ยวได้"""
    #     # line = ''.join(x for x in line if x in string.printable)
    #     # print(line)
    #     print(detect_lang(line))

    lst = ["Hyderabad"]
    print(detect_lang_list(["मुंबईः प्रतिनिधी हैद्राबाद येथील एका तरूण महिला डॉक्टरवर बलात्कार करून तीला जाळल्याप्रकरणी अटक करण्य"]))

    print("time ms:", (time() - x) * 1000)
