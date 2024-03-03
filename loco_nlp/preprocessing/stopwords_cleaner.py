import re
from loco_nlp.preprocessing.space_cleaner import clean_spaces
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_stopwords(text):
    stopWords = set(stopwords.words('english'))
    counter = lambda text: [w for w in word_tokenize(text) if w in stopWords]
    return list(map(counter, text)) if type(text) is list else counter(text)


def clean_stop_words(text, replacement=None):
    def detector(input_text):
        stopWords = set(stopwords.words('english'))
        words = re.split("[\W]+", text)
        split_words = re.split("[\w]+", text)
        final_text = []
        for split_word, word in zip(split_words, words):
            final_text.append(split_word)
            if word in stopWords:
                final_text.append(' ')
            else:
                final_text.append(word)
        return clean_spaces(''.join(final_text))

    return list(map(detector, text)) if type(text) is list else detector(text)


if __name__ == "__main__":
    print("ok")
    print(clean_stop_words("She went to the.s market to get potatoes to."))
