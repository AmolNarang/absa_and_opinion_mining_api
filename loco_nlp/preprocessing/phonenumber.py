import phonenumbers
from loco_nlp.config import REPLACEMENTS


def extract_phonenumber(text):
    def replace_phonenumber(sentence):
        result = []
        for match in phonenumbers.PhoneNumberMatcher(sentence, 'IN'):
            result.append(match.raw_string)
        return result

    return list(map(replace_phonenumber, text)) if type(text) is list else replace_phonenumber(text)


def clean_phonenumber(text, replacement=REPLACEMENTS['contact_number']):
    def replace_phonenumber(sentence):
        for match in phonenumbers.PhoneNumberMatcher(sentence, 'IN'):
            new_sentence = sentence.replace(match.raw_string, replacement).strip()
            if new_sentence:
                sentence = new_sentence

        return sentence

    return list(map(replace_phonenumber, text)) if type(text) is list else replace_phonenumber(text)


if __name__ == "__main__":
    print("ok")
    print(extract_phonenumber('test 9801234567 9812345678'))
    print(extract_phonenumber(['test 9801234567', 'test 2 9812345678']))
