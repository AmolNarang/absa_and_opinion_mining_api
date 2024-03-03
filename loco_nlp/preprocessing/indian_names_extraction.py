import json
import re

from loco_nlp.preprocessing.tokenizer import tokenize_word
from loco_nlp.config import BASE_PATH
from loco_nlp.tools.tokenizer import organic_split


class IndianNamesExtraction:
    def __init__(self, indian_name=None):
        if indian_name:
            self.indian_name = indian_name
        else:
            with open(f"{BASE_PATH}/data/required/indian_names_dict.json", "r") as fp:
                self.indian_name = json.load(fp)
        self.replacement = 'nnaammee'

    def detect_one(self, input_text):
        tokenised_text = organic_split(input_text)
        if len(tokenised_text) == 0:
            return []
        else:
            names = []
            connected_name = False
            for word in tokenised_text:
                if len(word) > 2 and word.lower() in self.indian_name:
                    if connected_name:
                        names[-1] = names[-1] + " " + word
                    else:
                        names.append(word)
                    connected_name = True
                else:
                    connected_name = False
        return names

    def replace_one(self, text):
        words = organic_split(text)
        for word_, word in enumerate(words):
            if len(word) > 2 and word.lower() in self.indian_name:
                words[word_] = self.replacement
        text = "".join(words)
        pattern = re.compile(f"({self.replacement}) \1{1,}")
        text = pattern.sub(r"\1", text)
        return text

    def detect(self, texts):
        if type(texts) is list:
            return list(map(self.detect_one, texts))
        else:
            return self.detect_one(texts)

    def replace(self, texts, replacement='nnaammee'):
        self.replacement = replacement
        if type(texts) is list:
            return list(map(self.replace_one, texts))
        else:
            return self.replace_one(texts)


if __name__ == "__main__":
    indian_name_ext = IndianNamesExtraction()
    print(indian_name_ext.detect(
        "Dear Jamaluddin, We continuously work towards providing you with a great experience. Glad to know that you are enjoying the Home Credit app. Have a nice day! Best Wishes, Home Credit India"))
    print(indian_name_ext.replace(
        "Dear Jamaluddin, We Jamaluddin continuously work towards providing you with a great experience. Glad to know that you are enjoying the Home Credit app. Have a nice day! Best Wishes, Home Credit India"))
