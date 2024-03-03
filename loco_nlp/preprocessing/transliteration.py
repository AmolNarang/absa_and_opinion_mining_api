import json
from loco_nlp.tools.tokenizer import organic_split
from loco_nlp.config import BASE_PATH


class HindiTransliteration(object):
    def __init__(self):
        with open(f"{BASE_PATH}/data/required/hindi_transliteration_wordmap.json", "r") as fp:
            self.hindi_transliteration_wordmap = json.load(fp)

    def hinglish_to_hindi(self, text):
        text = organic_split(text)
        for index, word in enumerate(text):
            word = word.lower()
            if word in self.hindi_transliteration_wordmap.keys():
                text[index] = self.hindi_transliteration_wordmap[word]
        text = "".join(text)
        return text


if __name__ == "__main__":
    print('ok')
    ht = HindiTransliteration()
    print(ht.hinglish_to_hindi("kya baat hai ye toh best hai"))