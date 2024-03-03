from loco_nlp.preprocessing.url_cleaner import clean_url
from loco_nlp.preprocessing.clean_numbers import clean_numbers
from loco_nlp.preprocessing.email_cleaner import clean_email
from loco_nlp.preprocessing.phonenumber import clean_phonenumber
from loco_nlp.preprocessing.hashtag_cleaner import clean_hashtags
from loco_nlp.preprocessing.username_cleaner import clean_username
from loco_nlp.preprocessing.primary_preprocessor import primary_punct_cleaning
from loco_nlp.preprocessing.hinglish_detector import HinglishDetector
from loco_nlp.preprocessing.ner_cleaner import NERCleaner
from loco_nlp.preprocessing.emoji_cleaner import EmojiCleaner
import spacy


class Cleaner:
    def __init__(self, spacy_model=None):
        self.moji = EmojiCleaner()
        self.nclean = NERCleaner(doc_nlp=spacy_model)
        self.hinglish = HinglishDetector()

    def cleaner(self, text):
        text = clean_url(text)
        text = self.moji.clean_emoji(text)
        text = clean_phonenumber(text)
        text = clean_email(text)
        text = clean_hashtags(text, '')
        text = clean_username(text)
        text = primary_punct_cleaning(text)
        text = clean_numbers(text)
        is_hinglish = self.hinglish.detect(text)
        if is_hinglish:
            result = text.lower()
            return result
        else:
            text = self.nclean.clean_NER(text)
            result = text.lower()
            return result

    def generic_cleaning(self, input_text):
        return list(map(self.cleaner, input_text)) if type(input_text) is list else self.cleaner(input_text)


if __name__ == '__main__':
    print('ok')
    gc = Cleaner()
    gc.doc_nlp = spacy.load("en_core_web_sm")
    # print(gc.generic_cleaning('Love you 3000, test this sentence, I am feeling good, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com'))
    # print(gc.generic_cleaning(['😀😀😀White ❤❤🐘❤❤ Purple Heart FlagFogg#','Love you 3000, test this sentence, I am feeling good, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com']))
    print(gc.generic_cleaning(['Hi how are Google']))



