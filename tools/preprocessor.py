import re
import json

from config import BASE_DATA_PATH

def preprocess(data, LANGUAGE_CODE, metadata_lang, emoji_data_lang):
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~`" + '""“”’' + '∞θ÷α•−β∅³π‘₹´°£€\×™√²—–&'

    def clean_special_chars(text, metadata_lang, punct, emoji_data_lang):
        text = re.sub(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))',
            metadata_lang.get('link', ' '), text)
        text = re.sub(r'@[\w]+', metadata_lang.get('username', ' '), text)
        text = re.sub(r'#[\w]+', metadata_lang.get('tag', ' '), text)
        text = re.sub(r'\d+', "10", text)

        for i in text:
            if i in emoji_data_lang.keys():
                text = text.replace(i, " ")  # emoji_data_lang[i])

        if LANGUAGE_CODE == 'en':
            text = text.lower()
        for search_text, replace_text in [
            ('?', ' '),
            ('!', ' '),
            ('.', ' '),
            ("what's", "what is"),
            ("'ve", " have "),
            ("can't", "can not"),
            ("n't", " not"),
            ("i'm", "i am "),
            ("'re", " are"),
            ("'d", " would"),
            ("'ll", " will"),
            (" ll ", " will "),
            ("'s", " ")
        ]:
            text = text.replace(search_text, replace_text)

        if LANGUAGE_CODE not in ['th']:
            text = re.sub('[\ \n]+', ' ', text)
            for p in punct:
                text = text.replace(p, ' ')

        if LANGUAGE_CODE in ['th']:
            text = re.sub(r'[A-Za-z\ \t\n]+', '', text)

        text = text.strip()
        return text

    data = list(map(lambda x: clean_special_chars(x, metadata_lang, punct, emoji_data_lang), data))
    return data


def preprocessor(data, lang, meta_data=None, emoji_data=None):
    if not emoji_data:
        with open(f"{BASE_DATA_PATH}/dataset/emoji_translation.json", "r") as fp:
            emoji_data = json.load(fp)

    return preprocess(data, lang, {}, emoji_data.get(lang, {}))


def herf_cleaner(text_lst):
    clean_text = []
    for text in text_lst:
        text = re.sub(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))', '', text)
        text = re.sub(r'@[\w]+', ' ', text)
        conv_text = re.sub(r'#[\w]+', ' ', text)
        conv_text = re.sub(r'\d+', ' ', conv_text)
        conv_text = conv_text.strip()
        if len(conv_text) < 12:
            conv_text = re.sub(r'#', ' ', text)
            conv_text = re.sub(r'\d+', ' ', conv_text)
            conv_text = conv_text.strip()
            clean_text.append(conv_text)
        else:
            clean_text.append(conv_text)

    return clean_text


if __name__ == "__main__":
    #print(preprocessor(["hey @hu #sdfj, https://google.com ", "test"], 'es'))

    print(herf_cleaner([ '#appreciationpost from our clients😇\n.\n.\n.\n.\n.\n.\n#happyus #sunitasarmalkar\n#homedeliveryservice #happyclient #hardworkpaysoffs @ lower parel https://t.co/3zhgccigdi']))
