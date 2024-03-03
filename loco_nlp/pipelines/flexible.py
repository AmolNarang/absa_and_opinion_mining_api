from loco_nlp.preprocessing.url_cleaner import clean_url
from loco_nlp.preprocessing.clean_numbers import clean_numbers
from loco_nlp.preprocessing.email_cleaner import clean_email
from loco_nlp.preprocessing.extended_words_cleaner import extract_extended_words
from loco_nlp.preprocessing.phonenumber import clean_phonenumber
from loco_nlp.preprocessing.hashtag_cleaner import clean_hashtags
from loco_nlp.preprocessing.username_cleaner import clean_username
from loco_nlp.preprocessing.primary_preprocessor import all_punct_cleaning
from loco_nlp.preprocessing.word_segment import segment_words
from loco_nlp.preprocessing.space_cleaner import clean_spaces
from loco_nlp.preprocessing.extended_words_cleaner import clean_extended_words
from loco_nlp.preprocessing.hashtag_cleaner import extract_hashtags
from loco_nlp.preprocessing.lengthy import lengthy
from loco_nlp.preprocessing.noisy import clean_noisy_words
from loco_nlp.preprocessing.contraction import contraction_handler
from loco_nlp.preprocessing.word_clipper import clip
from loco_nlp.preprocessing.stopwords_cleaner import clean_stop_words
from loco_nlp.preprocessing.indian_names_extraction import IndianNamesExtraction
from loco_nlp.preprocessing.lemmatizing import Lemmatizing
from loco_nlp.preprocessing.stemming import Stemming
from loco_nlp.preprocessing.ner_cleaner import NERCleaner
from loco_nlp.preprocessing.emoji_cleaner import EmojiCleaner
from loco_nlp.preprocessing.transliteration import HindiTransliteration
import spacy

stem = Stemming()
lem = Lemmatizing()


all_func = ['url', 'emoji', 'phonenumber', 'hashtag', 'hashtag_splitter', 'username', 'punct', 'number', 'lengthy', 'ner',
            'lower', 'stem', 'lemmatize', 'spaces', 'extended', 'contraction', 'to_hindi', 'noisy', 'indian_names', 'email',
            'clip', 'stopwords']


class FlexibleCleaner:
    """
    Note: To get a list of all operations, you can call method get_operations.

    To customize the functions you can pass 'apply' as an argument to the class definition as follows:

    apply = [
    ["url", ['string to replace url'], {'replacement': "_replacement_word_"}],
    ["emoji", ['string to replace emoji], {'replacement': "_replacement_dict_"}],
    ["phonenumber", ['string to replace phone number'], {'replacement': "_replacement_word_"}],
    ["hashtag", ['Nothing to pass'], {'Nothing to pass'}],
    ['hashtag_splitter', ['Nothing to pass'], {'Nothing to pass'}],
    ["username", ['string to replace usernames'], {'replacement': "_replacement_word_"}],
    ["punct", ['List of punctuations you want to keep, others will be REPLACED WITH SPACE'], {'punct':'list of punctuations'}],
    ["number", ['String to replace numbers'], {'replacement': "_replacement_word_"}],
    ["ner", [Dict to map], {'entity_replacement_dict': "_replacement_dict"}],
    ["lower", ['Nothing'], {'Nothing}],
    ['stem',[Nothing],{Nothing}],
    ['lengthy',[Nothing],{Nothing}],
    ['lemmatize',[Nothing],{Nothing}],
    ['spaces',[Nothing],{Nothing}],
    ['extended',[Nothing],{Nothing}],
    ['contraction', [Nothing], {Nothing}],
    ['to_hindi', [Nothing], {Nothing}],
    ['noisy', [Nothing],{Nothing}],
    ['indian_names','string to replace',{'replacement': 'replacement_word'}],
    ['email',['String to replace'],{'replacement': "_replacement_word_"}].
    ['clip',[Nothing],[Nothing],
    ['stopwords'],[Nothing],[Nothing]]
]

    """
    ops_to_function = {
        "url": "clean_url",
        "emoji": "self.moji.sentiment_emoji_cleaner",
        "phonenumber": "clean_phonenumber",
        "email": "clean_email",
        "hashtag": "clean_hashtags",
        "hashtag_splitter": "extract_hashtags",
        "username": "clean_username",
        "punct": "all_punct_cleaning",
        "number": "clean_numbers",
        "ner": "self.nclean.clean_NER",
        'stem': 'stem.stem_words',
        'lemmatize': 'lem.lemmatize_words',
        'lengthy': 'lengthy',
        'spaces': 'clean_spaces',
        'extended': 'clean_extended_words',
        'contraction': 'contraction_handler',
        'to_hindi': 'self.ht.hinglish_to_hindi',
        'indian_names': 'self.ine.replace',
        'noisy': 'clean_noisy_words',
        "lower": "lambda x: list(map(lambda y: str(y).lower(), x)) if type(x) is list else x.lower()",
        'clip': 'clip',
        'stopwords': 'clean_stop_words'
    }

    all_cleaner = [
        ["url", [], {}],
        ["emoji", [], {}],
        ["phonenumber", [], {}],
        ["hashtag", [], {}],
        ['hashtag_splitter', [], {}],
        ["username", [], {}],
        ["punct", [], {}],
        ["number", [], {}],
        ["lengthy", [], {}],
        ["ner", [], {}],
        ["lower", [], {}],
        ['stem', [], {}],
        ['lemmatize', [], {}],
        ['spaces', [], {}],
        ['extended', [], {}],
        ['contraction', [], {}],
        ['to_hindi', [], {}],
        ['noisy', [], {}],
        ['indian_names', [], {}],
        ['email', [], {}],
        ['clip', [], {}],
        ['stopwords', [], {}]
    ]

    def __init__(self, spacy_model=None, apply=None):
        self.apply = apply if apply else self.all_cleaner
        self.moji = EmojiCleaner()
        self.nclean = NERCleaner(doc_nlp=spacy_model)
        self.lem = Lemmatizing()
        self.stem = Stemming()
        self.ht = HindiTransliteration()
        self.ine = IndianNamesExtraction()

        assert type(self.apply) == list, 'The argument passed to the class should be of type list.'
        for i in self.apply:
            assert type(i) == list, 'Please check format of the operations passed.'
            assert len(i) == 3, 'Please enter all the arguments for the function'
            assert type(i[0]) == str, 'Please check the name of the operations passed'
            assert i[0] in all_func, 'Please enter a valid operation'
            assert type(i[1]) == list, 'An operation is missing argument block'
            assert type(i[2]) == dict, 'Please enter a valid kwargs argument for the operation'

    def get_operations(self):
        return list(self.ops_to_function.keys())

    def clean(self, text):
        for operation in self.apply:
            # try:
            text = eval(str(self.ops_to_function.get(operation[0])))(text, *operation[1], **operation[2])
            # except Exception as e:
            # pass
        return text

    def generic_cleaning(self, input_text):
        return list(map(self.cleaner, input_text)) if type(input_text) is list else self.cleaner(input_text)


if __name__ == '__main__':
    print('ok')
    # gc = FlexibleCleaner(apply=[["url", ['lalit'], {}],
    #                    ["emoji", [''], {}],
    #                    ["phonenumber", [''], {}],
    #                    ["hashtag", [''], {}],
    #                    ['hashtag_splitter', [], {}],
    #                    ['email', [''], {}],
    #                    ['username', [''], {}],
    #                    ['punct', [], {}],
    #                    ['number', [''], {}],
    #                    ['extended', [], {}],
    #                    ['ner', [], {}],
    #                    ['lemmatize', [], {}],
    #                    ['stem', [], {}],
    #                    ['spaces', [], {}],
    #                    ['lower', [], {}]])

    gg = FlexibleCleaner(apply=[['url', [], []], ['spaces',[],{}]])

    #gg = FlexibleCleaner()
    print(gg.__doc__)
    # print(gc.cleaner(
    #    'muze job chahiye, test caaaarrrrrrrr this sentence, I am feeling good, I am @Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com https://chat.google.com/dm/l4iNigAAAAE'))
    # print(gc.cleaner(['😀😀😀White ❤❤🐘❤❤ Purple Heart #FlagFogg',
    #                  'Love you 3000, test this sentence, I am feeling good, I am @Groot and I am working in Google. My number is 9807654321 and mail id is abc@gmail.com']))
    print(gg.clean('She went to the market to get vegetables.'))
    print(gg.all_cleaner)
