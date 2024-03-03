import json
from loco_nlp.preprocessing.tokenizer import tokenize_word


class NGram:
    def __init__(self, n_level, ngram={}):
        self.ngram = ngram
        self.n_level = n_level

    def preprocessor(self, texts):
        for text_, text in enumerate(texts):
            text = str(text).lower()
            text = text.replace(u'\xa0', u' ')
            texts[text_] = text
        texts = tokenize_word(texts)
        return texts

    def normalize_ngram(self, ngram=None):
        if ngram is None:
            ngram = self.ngram

        total_count = 0
        for word in ngram.keys():
            if word != "_":
                total_count += ngram[word].get("_", 0)

        for word in ngram.keys():
            if word != "_":
                ngram[word]['_'] = ngram[word]['_'] / total_count
                ngram[word] = self.normalize_ngram(ngram[word])

        return ngram

    def fit(self, texts, weights=1):
        for text in self.preprocessor(texts):
            text_len = len(text)
            for word_, word in enumerate(text):
                if word not in self.ngram:
                    self.ngram[word] = {"_": weights}
                else:
                    self.ngram[word]["_"] += weights

                temp = self.ngram[word]

                if text_len >= (word_ + self.n_level):
                    lst = text[(word_ + 1):(word_ + self.n_level)]
                else:
                    lst = text[(word_ + 1):]
                for sub_word in lst:
                    if sub_word not in temp:
                        temp[sub_word] = {"_": weights}
                    else:
                        temp[sub_word]["_"] += weights

                    temp = temp[sub_word]

    def fit_finalization(self):
        self.ngram = self.normalize_ngram(self.ngram)

    def save(self, path):
        with open(path, "w") as fp:
            json.dump({
                "ngram": self.ngram
            }, fp=fp)

    def load(self, path):
        data = json.load(open(path))
        self.ngram = data['ngram']


if __name__ == "__main__":
    n = NGram(5)
    n.fit(["this is not a good way to do anything in the world of coding"])
    print(n.ngram)
