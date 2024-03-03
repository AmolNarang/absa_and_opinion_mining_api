import re
from loco_nlp.config import REPLACEMENTS


def extract_username(text):
    extractor = lambda sentence: re.findall(r'@[a-zA-Z0-9_]{0,15}', sentence)
    return list(map(extractor, text)) if type(text) is list else extractor(text)


def clean_username(text, replacement=REPLACEMENTS['user_name']):
    replacer = lambda sentence: re.sub(r'(rt\ @[\w]+:)|(@[\w]+)', replacement, sentence).strip()
    return list(map(replacer, text)) if type(text) is list else replacer(text)


if __name__ == "__main__":
    print(clean_username('test rt @user:'))
    print(clean_username('test @user'))
    print("ok")