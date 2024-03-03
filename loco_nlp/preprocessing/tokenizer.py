from nltk.tokenize import sent_tokenize, word_tokenize


def tokenize_word(text_list, lang='en'):
    if type(text_list) is list:
        tokenized_text = list(map(word_tokenize, text_list))
    else:
        tokenized_text = word_tokenize(text_list)
    return tokenized_text


def tokenize_sentence(text_list, lang='en'):
    if type(text_list) is list:
        tokenized_text = list(map(sent_tokenize, text_list))
    else:
        tokenized_text = sent_tokenize(text_list)
    return tokenized_text


if __name__ == "__main__":
    print("ok")
    print(tokenize_sentence("this is text. this in not text"))
    print(tokenize_word('incredibleindia,ujjain,mptourism,holy'))


