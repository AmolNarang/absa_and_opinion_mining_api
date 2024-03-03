import numpy as np
from scipy import spatial


class Similarity:
    score = 0
    path = "/home/user/Projects/word_embedding/completed/cc.en.300.vec"
    similarity_map = {}

    def __init__(self, file_path=None):
        if file_path:
            self.path = file_path
        self.similarity_map = self.load_embeddings()

    def get_coefs(self, word, *arr):
        return word, np.asarray(arr, dtype='float32')

    def load_embeddings(self):
        with open(self.path) as self.file:
            return dict(self.get_coefs(*line.strip().split(' ')) for line in self.file)

    def get_word_vector(self, word1):
        if word1 in self.similarity_map:
            return self.similarity_map[word1]
        else:
            return list(np.zeros(300))

    def cosine_similarity(self, word1, word2):
        vec1 = self.get_word_vector(word1)
        vec2 = self.get_word_vector(word2)
        return 1 - spatial.distance.cosine(vec1, vec2)


if __name__ == '__main__':
    sm = Similarity()
    print('ok')
    print(sm.cosine_similarity("dog", "han"))
    print(sm.cosine_similarity("dog", "han"))
    sm.cosine_similarity("dog", "cat")