import contractions
from loco_nlp.config import DEFAULT_LANGUAGE


def simplify(text, lang=DEFAULT_LANGUAGE):
    return list(map(contractions.fix, text)) if type(text) is list else contractions.fix(text)


if __name__ == "__main__":
    print("ok")
    print(simplify('test Thats why I like python'))
    print(simplify(["test Thats why I like python", "couldn't"]))