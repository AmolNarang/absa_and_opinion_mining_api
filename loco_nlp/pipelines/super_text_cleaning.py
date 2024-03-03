from loco_nlp.preprocessing.url_cleaner import clean_url
from loco_nlp.preprocessing.clean_numbers import clean_numbers
from loco_nlp.preprocessing.email_cleaner import clean_email
from loco_nlp.preprocessing.phonenumber import clean_phonenumber
from loco_nlp.preprocessing.hashtag_cleaner import clean_hashtags
from loco_nlp.preprocessing.username_cleaner import clean_username
from loco_nlp.preprocessing.emoji_cleaner import EmojiCleaner
from loco_nlp.preprocessing.primary_preprocessor import all_punct_cleaning

class SuperCleaning:
    def __init__(self):
        self.moji = EmojiCleaner()

    def super_cleaner(self, input_text):
        def cleaner(text):
            text = clean_url(text, replacement='')
            text = clean_hashtags(text, replacement='')
            text = self.moji.clean_emoji(text)
            text = clean_phonenumber(text, replacement='')
            text = clean_email(text, replacement='')
            text = clean_username(text, replacement='')
            text = clean_numbers(text, replacement='')
            text = all_punct_cleaning(text)
            result = text.lower()

            return result

        return list(map(cleaner, input_text)) if type(input_text) is list else cleaner(input_text)


if __name__ == '__main__':
    print('ok')
    hc = SuperCleaning()
    print(hc.super_cleaner('Love you 3000, test this sentence, I am #feelinggood, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com'))
    print(hc.super_cleaner(['Love you 3000, test this sentence.!?,, I am #feelinggood, I am Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com', 'This is another text', ' ']))
