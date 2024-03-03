import re
import json
from loco_nlp.config import BASE_PATH
from loco_nlp.preprocessing.space_cleaner import clean_spaces
with open(f'{BASE_PATH}/data/required/word_embedding_words.json', 'r') as json_file:
    english_embedding = json.load(json_file)

def clean_noisy_words(text, replacement=None):
    def detector(input_text):
        ner_rep = ['oorrgg', 'ppeerrssoonn', 'llooccaattiioonn']

        words = re.split("[\W]+", input_text)
        split_words = re.split("[\w]+", input_text)

        final_text = []
        for split_word, word in zip(split_words, words):
            final_text.append(split_word)
            if word not in english_embedding:
                if word not in ner_rep:
                    final_text.append(' ')
            else:
                final_text.append(word)
        return clean_spaces(' '.join(final_text))

    return list(map(detector, text)) if type(text) is list else detector(text)


if __name__ == "__main__":
    print("ok")
    print(clean_noisy_words("jksdnn skdlngvlksdn sdnffklsdn sister couldn, t attend Jeff's party because she didn't study."))
