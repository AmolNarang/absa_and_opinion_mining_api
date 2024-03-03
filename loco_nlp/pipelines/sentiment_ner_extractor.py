from loco_nlp.preprocessing.url_cleaner import clean_url
from loco_nlp.preprocessing.clean_numbers import clean_numbers
from loco_nlp.preprocessing.email_cleaner import clean_email
from loco_nlp.preprocessing.phonenumber import clean_phonenumber
from loco_nlp.preprocessing.word_segment import segment_words
from loco_nlp.preprocessing.username_cleaner import clean_username
from loco_nlp.preprocessing.emoji_cleaner import EmojiCleaner
from loco_nlp.preprocessing.primary_preprocessor import primary_punct_cleaning
from loco_nlp.preprocessing.ner_detector import NERDetector

class SentimentNER:
    def __init__(self):
        self.moji = EmojiCleaner()
        self.ndetect = NERDetector()

    def ner_detection(self, input_text):
        def detector(text):
            text = clean_url(text, replacement='')
            text = segment_words(text)
            text = self.moji.sentiment_emoji_cleaner(text)
            text = clean_phonenumber(text, replacement='')
            text = clean_email(text, replacement='')
            text = clean_username(text, replacement='')
            text = clean_numbers(text)
            text = primary_punct_cleaning(text)
            result = self.ndetect.detect_NER(text)

            return result

        return list(map(detector, input_text)) if type(input_text) is list else detector(input_text)


if __name__ == '__main__':
    print('ok')
    sc = SentimentNER()
    print(sc.ner_detection('Love you 3000, test this sentence, I am #feelinggood, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com'))
    print(sc.ner_detection(['Love you 3000, test this sentence, I am #feelinggood, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com', 'This is another text', ' ']))
