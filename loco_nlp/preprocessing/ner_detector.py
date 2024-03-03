import spacy
from loco_nlp.config import REPLACEMENTS


class NERDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg", Disable=['tagger', 'parser'])

    def detect_NER(self, text_list):
        def detector(sentence):
            ner_dict = {
                'location': [],
                'person': [],
                'organisation': []
            }
            doc = self.nlp(sentence)
            for entity in doc.ents:
                if entity.label_ == 'PERSON':
                    ner_dict['person'].append(entity.text)
                elif entity.label_ == 'ORG':
                    ner_dict['organisation'].append(entity.text)
                elif entity.label_ == 'LOC' or entity.label_ == 'GPE' or entity.label_ == 'FAC':
                    ner_dict['location'].append(entity.text)

            return ner_dict

        return list(map(detector, text_list)) if type(text_list) is list else detector(text_list)


if __name__ == "__main__":
    print("ok")
    # %%timeit
    ner = NERDetector()
    print(ner.detect_NER('job chahiye'))
    print(ner.detect_NER(['AU Small Finance Bank mobile number send me I AM Sri Vijay Nagar Raj.ok']))
