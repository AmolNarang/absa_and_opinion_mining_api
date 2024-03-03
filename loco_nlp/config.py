# default values
# print(globals())

BASE_PATH = "/".join(__file__.split("/")[:-1])
DEFAULT_LANGUAGE = "en"
NGRAM_LANG = ["en"]

# ALL_LANG = {
#     # "zh": "chinese",
#     # "sd": "sindhi",
#     # "el": "greek",
#     # "ja": "japanese",
#     # "ko": "korean",
#     # "ne": "nepali",
#     "th": "thai",
#     # "fil": "filipino",
#     # "as": "assamese",
#     "bn": "bengali",
#     "da": "danish",
#     "de": "german",
#     "ga": "irish",
#     "gu": "gujarati",
#     "it": "italian",
#     "mr": "marathi",
#     "nl": "dutch",
#     # "or": "oriya",
#     "pl": "polish",
#     "pt": "portuguese",
#     "ru": "russian",
#     "te": "telugu",
#     "tr": "turkish",
#     "uk": "ukrainian",
#     "ur": "urdu",
#     "ar": "arabic",
#     "en": "english",
#     "es": "spanish",
#     "hi": "hindi",
#     "id": "bahasa",
#     "si": "sinhala",
#     "ta": "tamil",
#     # "ast": "asturian",
#     # "bh": "bihari",
#     "fr": "french",
#     "kn": "kannada",
#     "pa": "punjabi",
#     "sv": "swedish",
#     "vi": "vietenemes",
#     # "ml": "malayalam"
# } if not DEBUG else {
#     "hi": "hindi",
#     "en": "english",
#     "mr": "marathi"
# }

REPLACEMENTS = {
    'number': ' 10 ',
    'contact_number': ' mmoobbiillee ',
    'email_id': ' eemmaaiill ',
    'emoji': ' ',
    'ORG': ' oorrgg ',
    'PERSON': ' ppeerrssoonn ',
    'LOC': ' llooccaattiioonn ',
    'GPE': ' llooccaattiioonn ',
    'FAC': ' llooccaattiioonn ',
    'url': ' uurrll ',
    'user_name': ' nnaammee ',
    'hashtag': ' ttaagg '
}

SENTIMENT_EMOJI_REPLACEMENT = {
            '😊': 'like',
            '😻': 'like',
            '😍': 'like',
            '😡': 'hate',
            '😠': 'hate',
            '😘': 'love',
            '😗': 'love',
            '😚': 'love',
            '😙': 'love',
            '💏': 'like',
            '💑': 'like',
            '😽': 'like',
            '😄': 'like',
            '❤': 'love',
            '♥': 'love',
            '💞': 'love',
            '💕': 'love',
            '🆘': 'hate',
            '💩': 'hate',
            '😣': 'dislike',
            '👿': 'dislike',
            '🤬': 'hate',
            '❓': 'dislike',
            '🙁': 'dislike',
            '😔': 'dislike',
            '👎': 'dislike',
            '😤': 'hate'
        }

CONJUNCTIONS = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so',
                'either', 'not only', 'also', 'neither', 'both',
                'whether', 'just as', 'as much', 'no sooner',
                'rather', 'than', 'whereas', 'that', 'whatever',
                'which', 'whichever', 'after', 'before', 'by the time',
                'since', 'till', 'until', 'when', 'whenever', 'while',
                'though', 'although', 'even though', 'whoever', 'whomever',
                'where', 'wherever', 'only if', 'unless', 'provided that',
                'assuming that', 'even if', 'in case', 'as though', 'as if',
                'because', 'since', 'so that', 'in order']
