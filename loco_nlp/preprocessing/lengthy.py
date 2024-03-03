import json
import re
from loco_nlp.config import BASE_PATH
from loco_nlp.models.word_segmentation.word_segmentation import WordSegmentation

w = WordSegmentation(['en'])

with open(f'{BASE_PATH}/data/required/word_embedding_words.json', 'r') as json_file:
    english_embedding = json.load(json_file)

with open(f'{BASE_PATH}/data/required/final_hinglish_wordmap.json') as json_file:
    hinglish_embedding = json.load(json_file)


def lengthy_handler(text):
    lengthy_words = re.findall("[\w]{15,}", text)
    if len(lengthy_words) != 0:
        not_english_words = [i for i in lengthy_words if i not in english_embedding]
        not_hinglish_words = [i for i in not_english_words if i not in hinglish_embedding]
        segmented_lengthy_words = w.predict('en', not_hinglish_words)
        for i, j in zip(not_hinglish_words, segmented_lengthy_words):
            text = text.replace(i, ' '.join(j))
        return text
    else:
        return text


def lengthy(text_lst, replacement=None):
    if type(text_lst) is list:
        segmented_text_lst = []
        for text in text_lst:
            sent = lengthy_handler(text)
            segmented_text_lst.append(sent)
        return segmented_text_lst
    else:
        return lengthy_handler(text_lst)


if __name__ == "__main__":
    print("ok")
    print(lengthy('SuccessfulIndianEconomy OneLifeOneLoveOneWorld technologically #SuccessfulIndianEconomy'))
    print(lengthy(['test #OneLifeOneLoveOneWorld #ILoveIndia #Thisistag OneLifeOneLoveOneWorld SuccessfulIndianEconomy technologically']))
    print(lengthy(['test #goodboy #ILoveIndia #Thisistag OneLifeOneLoveOneWorld technologically',
                  'OneSpiritOneLoveOneWorld technologically SuccessfulIndianEconomy']))