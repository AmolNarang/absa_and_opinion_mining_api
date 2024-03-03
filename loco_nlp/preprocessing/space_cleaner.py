import re


def clean_spaces(text, replacements=''):
    replacer = lambda text : re.sub("[\ \t\n]+", ' ', text).strip()
    return list(map(replacer, text)) if type(text) is list else replacer(text)

if __name__ == "__main__":
    print('ok')
    print(clean_spaces("    test #$^ .   '\n'      1dnf ! dsjngaj      > ?       "))
