from nltk.stem import WordNetLemmatizer
from loco_nlp.tools.tokenizer import organic_split

class Lemmatizing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def lemmatize_words(self, text, replacement=None):
        if type(text) is list:
            lemmatized_sentence = []
            for sent in text:
                tokens = organic_split(sent)
                words = [word for word in tokens if word != ' ']
                lemmatized_sentence.append(self.get_lemma(words).strip())
            return lemmatized_sentence
        else:
            tokens = organic_split(text)
            words = [word for word in tokens if word != ' ']
            return self.get_lemma(words).strip()

    def get_lemma(self, tokenized_list):
        lemmatized_words_list = list(map(self.lemmatizer.lemmatize, tokenized_list))
        sentence = ' '.join(lemmatized_words_list)
        return sentence


if __name__ == "__main__":
    print("ok")
    lt = Lemmatizing()
    print(lt.lemmatize_words('running'))
    print(lt.lemmatize_words('lovely hating making'))
    print(lt.lemmatize_words(['loving hating making', 'eating making']))