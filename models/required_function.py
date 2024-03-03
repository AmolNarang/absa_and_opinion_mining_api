import re
from transformers import pipeline
import torch
from transformers import T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import BASE_PATH, BASE_DATA_PATH
from optimum.onnxruntime import ORTModelForSeq2SeqLM
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

class OpinionExtractor:
    def __init__(self):
        self.model_name = "t5-small"
        self.T5_token_path = f"{BASE_PATH}/t5smalltokenizer"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.T5_token_path)
        self.output_model_dir = f"{BASE_DATA_PATH}/fine_tuned_model_2_combine3L_1"
        self.max_length = 64
        self.model_path = f"{BASE_DATA_PATH}/cardiff_nlp"
        self.tokenizer_1 = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"{BASE_DATA_PATH}/cardiff_nlp/tokenizer")
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        self.model_quantized = torch.quantization.quantize_dynamic(
            self.model.to("cpu"),
            {torch.nn.Linear},
            dtype=torch.qint8
        )
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=self.model_quantized, tokenizer=self.tokenizer_1)
        self.fine_tuned_model = T5ForConditionalGeneration.from_pretrained(self.output_model_dir)
        self.fine_tuned_model = self.fine_tuned_model.to(self.device)
        self.fine_tuned_model = ORTModelForSeq2SeqLM.from_pretrained(self.output_model_dir, from_transformers=True)

    def extract_opinion(self, aspects, input_string):

        input_string = re.sub(r',?\s*hashtag:?\s*', '', input_string)
        opinions = []
        if (len(aspects) == 0):
            return opinions
        for i in range(len(aspects) - 1):
            pattern = aspects[i] + ': ([^:]+), ' + aspects[i + 1] + ':'
            matches = re.findall(pattern, input_string)
            opinions.append(matches)
        # pattern = aspects[-1] + ': ([^:]+)'
        pattern = r'[^:]*:\s*((?!.*:).*)'
        matches = re.findall(pattern, input_string)
        opinions.append(matches)
        return opinions

    def extract_aspect(self, input_string):
        # input_string = input_string.replace(", hashtag: ", "")
        # input_string = input_string.replace(", hashtag:", "")
        # input_string = input_string.replace("hashtag:", "")
        # input_string = input_string.replace(", hashtag ", "")
        # input_string = input_string.replace(", hashtag", "")
        # input_string = input_string.replace("hashtag", "")
        input_string = re.sub(r',?\s*hashtag:?\s*', '', input_string)
        pattern = r', (?P<letters_between_space_and_colon>[^,:]+):'
        matches = re.findall(pattern, ", " + input_string)
        return matches

    def extract_input_texts_with_slide_2(self, step_size, window_size, ac_text):
        xlen = len(ac_text)
        input_texts = []
        # print(step_size,window_size)
        if xlen <= window_size:
            input_texts.append(ac_text)
            # print("here1")
            return input_texts
        else:
            # print("here2")
            start_ind = 0
            end_ind = window_size

            while end_ind <= xlen:
                # print(start_ind,end_ind,'1')
                # print("here3")
                input_texts.append(ac_text[start_ind:end_ind])
                # print(input_texts,"here3")
                start_ind += step_size
                end_ind += step_size
                # print(start_ind, end_ind,'2')
            input_texts.append(ac_text[start_ind:xlen])
        input_texts.append(ac_text)
        return input_texts

    def pred_out_with_slide(self, input_texts):
        input_ids = self.tokenizer(input_texts, return_tensors="pt",
                                   padding=True, truncation=True, max_length=self.max_length)['input_ids']
        input_ids = input_ids.to(self.device)

        with torch.no_grad():
            outputs = self.fine_tuned_model.generate(input_ids)

        predicted_output = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

        return predicted_output

    def asp_opn_pair_withslide(self, predicted_output):
        aspp1 = []
        oppp1 = []

        for sents in predicted_output:
            asp1 = self.extract_aspect(sents)
            aspp1.extend(asp1)
            oppp1.extend(self.extract_opinion(asp1, sents))

        # print("----->",aspp1)
        # print("----->",oppp1)
        return aspp1, oppp1

    def result_dic_withslide(self, aspp1, oppp1):
        result1 = {}

        for asp, opp in zip(aspp1, oppp1):
            if asp in result1:
                result1[asp].extend(opp)
            else:
                result1[asp] = opp

        result1_2 = {key: list(set(values)) for key, values in result1.items()}
        return result1_2

    def asp_opn_dic_result_withslide_2(self, step_size, window_size, ac_text):
        input_texts = self.extract_input_texts_with_slide_2(step_size, window_size, ac_text)
        # print(input_texts)
        # print(len(input_texts))
        predicted_output = self.pred_out_with_slide(input_texts)
        # print(predicted_output)
        aspect_withslide, opinion_withslide = self.asp_opn_pair_withslide(predicted_output)
        # print(aspect_withslide)
        # print(opinion_withslide)
        results = self.result_dic_withslide(aspect_withslide, opinion_withslide)
        # print(results)
        return results

    def sentiment_label(self, raw_label):
        if raw_label == 'LABEL_0':
            # return 'NEGATIVE'
            return 2
        elif raw_label == 'LABEL_1':
            # return 'NEUTRAL'
            return 0
        # return 'POSITIVE'
        return 1

    def finalResult_withslide(self, dicc):
        # dic2 = {key: (value, self.sentiment_label(self.sentiment_analyzer(', '.join(value))[0]['label']), round(self.sentiment_analyzer(
        #     ', '.join(value))[0]['score'], 3)) for i, (key, value) in enumerate(dicc.items())}
        dic2 = {key: (value, self.sentiment_label(self.sentiment_analyzer(', '.join(value))[0]['label'])) for
                i, (key, value) in enumerate(dicc.items()) if len(key) > 1}
        return dic2

    def cleantext(self, text):
        if not isinstance(text, str):
            return text
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        text = re.sub(r'(@\w+|#\w+|https?://\S+|www\.\S+|<.*?>)', '', text)
        text = text.lower()
        text = ' '.join(text.split())
        return text

    def remove_garbage(self, result):
        elements_to_remove = ['available', 'beautifully designed', 'lackluster', 'high', 'large, vibrant', 'impressive',
                              'impressive,', 'high,', 'beautifully designed, large, vibrant display, impressive camera']

        keys_to_filter = ['phone', 'price', 'battery life', 'display', 'camera']

        filtered_result = {key: [[value for value in values[0] if value not in elements_to_remove],
                                 values[1]] if key in keys_to_filter else values for key, values in
                           result.items()}
        filtered_result = {key: values for key, values in filtered_result.items() if values[0]}
        return filtered_result

    def lemmatization(self, dicc):
        try:
            if dicc:
                return {lemmatizer.lemmatize(key): [value[0], value[1], key] for key, value in dicc.items()}
            else:
                return dicc
        except Exception as e:
            print("error with lemmatization ", e)
            return dicc

    def all_words_are_nouns_or_punc(self, sentence):
        words = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        for _, tag in pos_tags:
            if not (tag.startswith('N') or tag in [',', '.', '?', '!', ';', ':', "'", '"', '-', '(', ')', '[', ']', '{',
                                                   '}', '/', '\\']):  # Check if the tag does not start with 'N' (noun)
                return False
        return True

    def filter_with_noun(self,opinions):
        if ((len(opinions) == 1) & (len(word_tokenize(re.sub('[^a-zA-Z0-9\s]', '', opinions[0]))) < 4)):

            if self.all_words_are_nouns_or_punc(opinions[0]):
                # print(len(opinions), len(word_tokenize(re.sub('[^a-zA-Z0-9\s]', '', opinions[0]))))
                return 3
            else:
                return 0
        else:
            return 0

    def other_opinion(self, dicc):
        try:
            if dicc:
                filter_dicc = {
                    key: [value[0], value[1],value[2]] if value[1] != 0 else [value[0], self.filter_with_noun(value[0]),value[2]]
                    for key, value in dicc.items()
                }
                return filter_dicc
            else:
                return dicc
        except Exception as e:
            print("error with finding others", e)
            return dicc

    @staticmethod
    def check_word_count(text: str) -> bool:
        if not isinstance(text, str):
            return True
        # Split the text into words
        words = text.split()

        # Check if the number of words is less than 5
        return len(words) >= 3

    def absa_model(self, text, lang):
        if lang == "en" and self.check_word_count(self.cleantext(text)):
            # result = self.remove_garbage(self.finalResult_withslide(self.asp_opn_dic_result_withslide_2(100, 200, self.cleantext(text))))
            # filtered_result = self.lemmatization(result)
            # filtered_result = self.other_opinion(filtered_result)
            # return filtered_result
            return self.remove_garbage(self.finalResult_withslide(self.asp_opn_dic_result_withslide_2(100, 200, self.cleantext(text))))
        else:
            return {}

    # def filter_en_text(self,text):
    #     if pure_en_detector(text)=="en":
    #         return text
    #     return ""
