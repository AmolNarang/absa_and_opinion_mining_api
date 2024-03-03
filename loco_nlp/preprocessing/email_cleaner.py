import re
from loco_nlp.config import REPLACEMENTS


def extract_email(text):
    extractor = lambda sentence: re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*[a-zA-Z0-9]", sentence)
    return list(map(extractor, text)) if type(text) is list else extractor(text)


def clean_email(text, replacement=REPLACEMENTS['email_id']):
    replacer = lambda sentence: re.sub(
        r'([a-zA-Z0-9\+\._\/&!][-a-zA-Z0-9\+\._\/&!]*)@(([a-zA-Z0-9][-a-zA-Z0-9]*\.)([-a-zA-Z0-9]+\.)*[a-zA-Z]{2,})',
        replacement, sentence).strip()
    return list(map(replacer, text)) if type(text) is list else replacer(text)


if __name__ == "__main__":
    print("ok")
    print(clean_email('test abc@gmail.com'))
    print(extract_email('test abc@gmail.com'))
