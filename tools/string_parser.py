import re


def hastags_extracter(text_lst):
    # todo try using lamda function
    hash_tags_lst = []
    for text in text_lst:
        hash_tags = re.findall(r"#([^\ \/\-'?!.,#$%\'()*+-/:;<=>@\[\\\]\^_`{|}~\।]+)", text)
        hash_tags_lst.append(hash_tags)

    return hash_tags_lst
