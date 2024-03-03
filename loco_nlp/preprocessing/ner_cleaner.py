import spacy
from loco_nlp.config import REPLACEMENTS
import re


class NERCleaner:
    def __init__(self, doc_nlp=None):
        if doc_nlp is not None:
            self.nlp = doc_nlp
        else:
            self.nlp = spacy.load("en_core_web_sm")

    def clean_NER(self, text_list, entity_replacement_dict=None):
        if entity_replacement_dict is None:
            entity_replacement_dict = REPLACEMENTS
        entity_replacement_dict_values = entity_replacement_dict.values()

        def position_replace(text, start, end, replace_text, comp=0):
            return text[:start + comp] + replace_text + text[end + comp:]

        def replace_NER(sentence):
            comp = 0
            sentence = re.sub(r'[\n\t\ ]+', ' ',sentence)
            doc = self.nlp(sentence)
            for entity in doc.ents:
                if entity.label_ in entity_replacement_dict and entity.text not in entity_replacement_dict_values:
                    sentence = position_replace(sentence, entity.start_char, entity.end_char,
                                                     entity_replacement_dict[entity.label_], comp)
                    comp += len(entity_replacement_dict[entity.label_]) - int(entity.end_char - entity.start_char)
            return sentence

        return list(map(replace_NER, text_list)) if type(text_list) is list else replace_NER(text_list)


if __name__ == "__main__":
    print("ok")
    # %%timeit
    ner = NERCleaner()
    print(ner.clean_NER('ndia,roar,turnupthevolume,travel,callofthewildmumbai,madhyapradeshtourism,wild,tiger,video,explore,majesticWhen the legend of Pench grants you an audience. To spot a tiger is Rare but to hear it roar is even rarer and surreal.\n#tiger#tigersofinstagram#video#roar#roaring#wild#wilderness#sony#sonyrx10#turnupthevolume#wander#travel#explore#majestic#pench#madhyapradeshtourism#incredibleindia#india#callofthewildmumbai @penchjunglecamp @sudester @anvi.84 @wildlifeindia @wildlifeplanet @indianwildlifeofficial'))
    print(ner.clean_NER(['FE CFO Awards: Sashi Jagdishan — Never off balanceSashi Jagdishan says the biggest challenge at HDFC Bank is living up to the standards that the lender has set for itself.']))