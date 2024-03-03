import re

try:
    from spellchecker import SpellChecker

    spell = SpellChecker()
except Exception as e:
    print("error in spellchecker contact aniket", e)
    spell = {}


def extract_extended_words(text):
    def detector(input_text):
        result = {}
        match = re.finditer(r'[a-z]*([a-z])\1{2}[a-z]*', input_text.lower())
        for item in match:
            result[input_text[item.start():item.end()]] = item.group()
        return list(result.keys())

    return list(map(detector, text)) if type(text) is list else detector(text)


def clean_extended_words(text):
    word_dict = {}

    def corrector(input_word):
        pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
        corrected = pattern.sub(r"\1\1", input_word)
        return spell.correction(corrected)

    def replacer(input_text):
        extended_words = extract_extended_words(input_text)
        if extended_words:
            for word in extended_words:
                word_dict[word] = corrector(word.lower())
            for key, value in word_dict.items():
                input_text = input_text.replace(key, value)
        return input_text

    return list(map(replacer, text)) if type(text) is list else replacer(text)


if __name__ == "__main__":
    print("ok")
    print(extract_extended_words('test MMMaaan caaaaar hellllppppp hard aaab abbbbb abbbbbc aaabbbb aaaabccccc'))
    print(
        clean_extended_words(['Test MMMaaan caaaAAR hELLllppppp hard aaab abbbbb abbbbbc aaabbbb aaaabccccc']))
