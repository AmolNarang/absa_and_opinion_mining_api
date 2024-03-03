import re
import json
from loco_nlp.preprocessing.space_cleaner import clean_spaces
from loco_nlp.config import REPLACEMENTS, BASE_PATH, SENTIMENT_EMOJI_REPLACEMENT

all_emoji = re.compile('''[\U00010000-\U0010ffff]|\u2139|\u26F9|\u23F0|\u23F3|\u2693|\u26A1|\u26D4|\u26EA|\u26F5|\u2694|
                \u26FA|\u2B55|\u2328|\u23CF|\u24C2|\u25B6|\u25C0|\u260E|\u2611|\u2618|\u261D|\u2620|\u2626|\u262A|\u2660|\u2764|\u2661|
                \u2663|\u2668|\u267B|\u267F|\u2699|\u26C8|\u26CE|\u26CF|\u26D1|\u26FD|\u2702|\u2705|\u270F|\u2763|\u2712|\u2714|\u2716|
                \u271D|\u2721|\u2728|\u3297|\u2757|\u2744|\u2747|\u274C|\u274E|\u27A1|\u27B0|\u27BF|\u2B50|\u3030|\u303D|\u265F|\u23F1|
                [\u25FB-\u25FE]|[\u2600-\u2604]|[\u2614-\u2615]|[\u2622-\u2623]|[\u262E-\u262F]|[\u2638-\u263A]|[\u2665-\u2666]|\u2049|
                [\u2692-\u2694]|[\u2696-\u2697]|[\u269B-\u269C]|[\u26A0-\u26A1]|[\u26B0-\u26B1]|[\u26C4-\u26C5]|[\u26D3-\u26D4]|\u1F9D1|
                [\u26E9-\u26EA]|[\u26F0-\u26F5]|[\u26F7-\u26FA]|[\u2708-\u2709]|[\u270C-\u270D]|[\u2733-\u2734]|[\u2753-\u2755]|\u26E9|
                [\u2763-\u2764]|[\u2934-\u2935]|[\u2B05-\u2B07]|[\u270A-\u270B]|[\u231A-\u231B]|[\u23E9-\u23EC]|[\u25FD-\u25FE]|\u2692|
                [\u2648-\u2653]|[\u26AA-\u26AB]|[\u26BD-\u26BE]|[\u26F2-\u26F3]|[\u2795-\u2797]|[\u2B1B-\u2B1C]|\u2663|\u2197|\u2198|\u2199|
                \u2196|\u2195|\u2194|\u2026|\u65533|\u1F46F|\u2642|\u00A9|\u25AC|\u25C6|[\uFFF0-\uFFFF]''', flags=re.UNICODE)


# to get a mapped dict for other language ==> {k: custom_dict[v] for k,v in SENTIMENT_EMOJI_REPLACEMENT.items()}
# Ex : custom_dict = {'love':'aaaaa',like':'bbbbbb','dislike':'cccccc','hate':'ddddd'}

class EmojiCleaner:

    def __init__(self):
        with open(f"{BASE_PATH}/data/required/all_emoji_data.json", "r") as fp:
            self.emoji_data = json.load(fp)
        self.re_emoji = all_emoji

    def clean_emoji(self, text, replacement=REPLACEMENTS['emoji']):
        replacer = lambda sentence: self.re_emoji.sub(replacement, sentence)
        return list(map(replacer, text)) if type(text) is list else replacer(text)

    def sentiment_emoji_cleaner(self, text, replacement=REPLACEMENTS['emoji']):
        if type(replacement) is dict:
            def emoji_replacer(input_text):
                for ch in input_text:
                    if ch in replacement.keys():
                        input_text = input_text.replace(ch, ' ' + replacement[str(ch)] + ' ').strip()
                input_text = self.clean_emoji(input_text)
                input_text = clean_spaces(input_text)
                return input_text

        else:
            def emoji_replacer(text):
                return self.clean_emoji(text, replacement)

        return list(map(emoji_replacer, text)) if type(text) is list else emoji_replacer(text)

    def emoji_to_text_replacement(self, text):
        def replacer(input_text):
            for ch in input_text:
                if ch in self.emoji_data.keys():
                    input_text = input_text.replace(ch, ' ' + self.emoji_data[str(ch)] + ' ').strip()
            return input_text

        return list(map(replacer, text)) if type(text) is list else replacer(text)

    def emoji_extractor(self, text):
        def extractor(input_text):
            emoji_list = []
            for ch in input_text:
                if ch in self.emoji_data.keys():
                    emoji_list.append(ch)
            return emoji_list

        return list(map(extractor, text)) if type(text) is list else extractor(text)


if __name__ == "__main__":
    print("ok")
    ec = EmojiCleaner()
    print(ec.sentiment_emoji_cleaner('😀White 💜 Purple Heart FlagFogg#', 'repp'))
    print(ec.sentiment_emoji_cleaner('😀White 💜 Purple Heart 😊 FlagFogg#', SENTIMENT_EMOJI_REPLACEMENT))
    # print(ec.sentiment_emoji_cleaner('😀White ❤ Purple Heart FlagFogg#'))
    # print(ec.clean_emoji(['😀White 💜 Purple Heart FlagFogg#']))
    # print(ec.sentiment_emoji_cleaner(['😀White ❤❤❤ Purple Heart FlagFogg#']))
    # print(ec.emoji_to_text_replacement(['😀😀😀White 💜 Purple Heart 🐘 FlagFogg#']))
    # print(ec.emoji_to_text_replacement(['😀😀😀White ❤❤🐘❤❤ Purple Heart FlagFogg#']))
    # print(ec.emoji_extractor(['😀😀😀White ❤❤🐘❤❤ Purple Heart FlagFogg#']))
