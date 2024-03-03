import json
from multiprocessing import Pool
import re

from loco_nlp.config import NGRAM_LANG, BASE_PATH


class WordSegmentation:
    allowed_lang = NGRAM_LANG
    ngram = {}

    def get_words(self, input_word, found_seq, score, lang):
        # todo add capability to read uppercase
        # print((input_word, found_seq, score))
        if not input_word or input_word == "":
            return [{
                "word": found_seq,
                "score": score / (len(found_seq) ** 1.5)  # need to optimize
            }]

        seq = []
        for i in range(len(input_word) + 1, 1, -1):
            if input_word[:i] in self.ngram[lang]:
                ngram_found = False

                ngram_score = self.ngram[lang][input_word[:i]]["_"] * (len(input_word[:i]) ** 1.6)
                if len(found_seq) > 0 and input_word[:i] in self.ngram[lang][found_seq[-1]]:
                    ngram_score = self.ngram[lang][found_seq[-1]][input_word[:i]] * 10 + ngram_score
                    ngram_found = True

                seq += self.get_words(
                    input_word[i:],
                    found_seq + [input_word[:i]],
                    score + ngram_score,
                    lang
                )

                # if ngram_found:
                #     break
        return seq

    def result_filter(self, input_data):
        lang, word = input_data

        if lang == "en" and len(word) < 30:
            words_with_delimeter = re.findall("[A-Za-z]+", word)
            if len(words_with_delimeter) > 1:
                return words_with_delimeter

            capital_words_link = re.findall("[A-Z]{1}[a-z]+", word)
            if len(capital_words_link) > 1:
                return [x.lower() for x in capital_words_link]

            word = str(word).lower()
            word = re.sub("[\d]+", "", word)

            try:
                result = self.get_words(word, [], 0, lang)
                # print(result)
                if len(result) > 0:
                    result = sorted(result, key=lambda x: x['score'], reverse=True)[0]['word']
                return result
            except Exception as e:
                pass

        return [word]

    def __init__(self, languages: list):
        for lang in languages:
            if lang in self.allowed_lang:
                self.ngram[lang] = json.load(open(f"{BASE_PATH}/data/required/word_segmentation/en/main.json"))['ngram']

    def predict(self, lang: str, words: list):
        if lang not in NGRAM_LANG:
            return [[i] for i in words]
        # p = Pool(8)
        result = list(map(self.result_filter, [(lang, word) for word in words]))
        # p.close()
        return result

    def hashtag_handler(self, text_lst, text_lang='en'):
        segmented_text_lst = []
        for text in text_lst:
            hash_tags = re.findall(r"\#[\w]+", text)
            segmented_tags = self.predict(text_lang, [i[1:] for i in hash_tags])
            for i, j in zip(hash_tags, segmented_tags):
                text = text.replace(i, ' '.join(j))
            segmented_text_lst.append(text)

        return segmented_text_lst


if __name__ == "__main__":
    from time import time

    w = WordSegmentation(["en"])
    a = time()
    print(w.predict("en", ["goodperson", "nicelife", "goodlife", "electionmaharashtra2019"]))
    a = (time() - a) * 1000

    w = WordSegmentation(["en"])
    print(w.predict("en", ["wonderful_places_to_go", "ThisIsHeaven", "electionmaharashtra2019", "nicelife"]))
    print(w.hashtag_handler(["Hi This is #textcheck\n", "I am #goodboy"]))
