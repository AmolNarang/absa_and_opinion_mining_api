import time
from models.required_function import OpinionExtractor
import warnings
# from loco_nlp.preprocessing.language_detector import detect_lang
# from loco_nlp.preprocessing.language_detector import pure_en_detector
warnings.filterwarnings("ignore")
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize

ABOP_extractor = OpinionExtractor()

'''sentiments=ABOP_extractor.sentiment_analyzer
print(sentiments("VERY BAD"))'''
# text_input = "car is slow and late later we find that anything is better but                                                                                                                                car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxuriouscar is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious car is luxurious"
text_input = "Leaving for Jakarta to take part in ASEAN related meetings. This includes the 20th ASEAN-India Summit, which focuses on a partnership we greatly cherish. I will also take part in the 18th East Asia Summit, which focuses on important developmental sectors like healthcare, environment and digital innovations.Leaving for Jakarta to take part in ASEAN related meetings. This includes the 20th ASEAN-India Summit, which focuses on a partnership we greatly cherish. I will also take part in the 18th East Asia Summit, which focuses on important developmental sectors like healthcare, environment and digital innovations."
'''print(detect_lang("kese ho aap"))
print(detect_lang("How are you"))
print(detect_lang("aap kidhar rehto ho aapka ghar kaha h ye dusra language detector h"))

# print(detect_lang_list("kese ho aap"))
# print(detect_lang_list("How are you"))
# print(detect_lang_list("aap kidhar rehto ho aapka ghar kaha h ye dusra language detector h"))
print("----------------")
print(pure_en_detector("kese ho aap"))
print(pure_en_detector("How are you"))
print(pure_en_detector("aap kidhar rehto ho aapka ghar kaha h ye dusra language detector h"))'''
'''start_time = time.time()
print(ABOP_extractor.absa_model(text_input,pure_en_detector(text_input)))
end_time=time.time()
print(end_time-start_time)'''
out = ABOP_extractor.absa_model(text_input,'en')
# result = [{f"text_{index}": ABOP_extractor.absa_model(text)} for index, text in enumerate(text_input)]
# # final_result = {
# #     "status": "successful",
# #     "result": result,
# #     "time_ms": int((time.time() - start_time) * 1000)
# # }
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("phone")


def lemmatization( dicc):
    try:
        if dicc:
            return {lemmatizer.lemmatize(key): value for key, value in dicc.items()}
        else:
            return dicc
    except:
        return dicc

def all_words_are_nouns_or_punc(sentence):
    words = word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    for _, tag in pos_tags:
        if not (tag.startswith('N') or tag in [',', '.', '?', '!', ';', ':', "'", '"', '-', '(', ')', '[', ']', '{', '}', '/', '\\']):  # Check if the tag does not start with 'N' (noun)
            print(sentence,"_NOT NOUN_",tag,_)
            return False
    print(sentence,"_NOUN OR PUNC_", tag,_)
    return True
sentences = [
    "sbi"
]
t1=time.time()
filtered_sentences = [sentence for sentence in sentences if not all_words_are_nouns_or_punc(sentence)]
t2=time.time()-t1
for sentence in filtered_sentences:
    print(sentence)
print(t2*1000)

t1=time.time()
x=all_words_are_nouns_or_punc("sbi employee contact number")
t2=time.time()-t1
print(x,t2*1000)

print("stop")
# s1=time.time()
# for x in ["phone","camera","price","display","battery life","services","billing","building","rating","charging"]:
#     print(lemmatizer.lemmatize(x))
# print((time.time()-s1)*1000)
# diction={'phone': 'excellent', 'camera': 'great', 'price': 'affordable', 'display': 'vibrant', 'battery life': 'long-lasting', 'services': 'efficient', 'billing': 'convenient', 'building': 'sturdy', 'rating': 'high', 'charging': 'fast'}
diction = {'card': (['actively using', 'still havent received,'], 2), 'services': (['in india'], 0)}
t1=time.time()
x=lemmatization(out)
t2=time.time()-t1
print(x,t2*1000)
print("jdnf")