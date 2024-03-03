from nltk.stem import PorterStemmer
from loco_nlp.tools.tokenizer import organic_split


class Stemming:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def stem_words(self, text, replacement=''):
        if type(text) is list:
            stemmed_sentence = []
            for sent in text:
                tokens = organic_split(sent)
                words = [word for word in tokens if word != ' ']
                stemmed_sentence.append(self.get_stem(words).strip())
            return stemmed_sentence
        else:
            tokens = organic_split(text)
            words = [word for word in tokens if word != ' ']
            return self.get_stem(words).strip()

    def get_stem(self, tokenized_list):
        stem_words_list = list(map(self.stemmer.stem, tokenized_list))
        sentence = ' '.join(stem_words_list)
        return sentence


if __name__ == "__main__":
    print("ok")
    st = Stemming()
    print(st.stem_words('running'))
    print(st.stem_words('loving hating making'))
    print(st.stem_words(['loving hating making', 'eating making']))
