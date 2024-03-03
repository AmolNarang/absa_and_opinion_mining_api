import re


def organic_split(text):
    words = re.split("[\W]+", text)
    split_words = re.split("[\w]+", text)

    final_text = []
    for split_word, word in zip(split_words, words):
        final_text.append(split_word)
        final_text.append(word)
    return final_text


if __name__ == "__main__":
    print(organic_split("hey neel, how do you do?"))