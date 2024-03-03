import json
from loco_nlp.preprocessing.tokenizer import tokenize_word
from loco_nlp.config import BASE_PATH


class HinglishDetector:
    def __init__(self):
        with open(f"{BASE_PATH}/data/required/final_hinglish_wordmap.json", "r") as fp:
            self.hinglish_word_map = json.load(fp)

    def __detect_one(self, input_text, thresh=0.3):
        hinglish_words = []
        tokenised_text = tokenize_word(input_text.lower())
        if len(tokenised_text) == 0:
            return False

        for word in tokenised_text:
            if word in self.hinglish_word_map:
                hinglish_words.append(word)

        if (len(hinglish_words) / len(tokenised_text)) >= thresh and len(tokenised_text) >= 8:
            return True
        elif (len(hinglish_words) / len(tokenised_text)) >= 0.4:
            return True
        return False

    def detect(self, text, thresh=0.3):
        return list(map(lambda x: self.__detect_one(x, thresh), text)) if type(text) is list else self.__detect_one(text, thresh)


if __name__ == "__main__":
    hd = HinglishDetector()
    print(hd.detect(text='Hindi Samajhta Hai Kya me are very a on good Mere Bhai', thresh=0.2))
    print(hd.detect(['Hindi Samajhta Hai Kya Tujhe Mere Bhai', 'Ye Model Hinglish Bhi Samajhta Hai', "hey bro I am doing good"], thresh=0.8))
    print("ok")
