import re
from loco_nlp.config import REPLACEMENTS

#Todo make extract numbers

def clean_numbers(text, replacement=REPLACEMENTS['number']):
    replacer = lambda sentence: re.sub(r'\d+', replacement, sentence)
    return list(map(replacer, text)) if type(text) is list else replacer(text)


if __name__ == "__main__":
    print("ok")
    print(clean_numbers('test 34523'))
