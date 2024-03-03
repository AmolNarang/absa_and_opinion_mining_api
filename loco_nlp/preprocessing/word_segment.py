from loco_nlp.models.word_segmentation import word_segmentation

w3 = word_segmentation.WordSegmentation(['en'])

def segment_words(text):
    return w3.hashtag_handler(text) if type(text) is list else w3.hashtag_handler([text])[0]


if __name__ == "__main__":
    print("ok")
    print(segment_words('#wonderfulplacestogoinspiredtravelsincredibleindiaworldwonderwanderlustermanaliheavenonearthadventureseekeradventuretimemanalidiariesbeautifulmomentuttrakhandtourismheartofindiawanderlustingexploringtheglobevacationlifeone'))
    print(segment_words(['test #goodboy #ILoveIndia #Thisistag']))
    w3.hashtag_handler(['test #goodboy #ILoveIndia #Thisistag'])