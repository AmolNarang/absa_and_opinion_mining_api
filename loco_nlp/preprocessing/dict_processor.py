def dict_sum(dic1: dict, dic2: dict):
    result = {}
    for k in set(list(dic1.keys()) + list(dic2.keys())):
        result[k] = dic1.get(k, 0) + dic2.get(k, 0)
    return result


def dict_softmax(dic: dict):
    total = sum(dic.values())
    for k, v in dic.items():
        dic[k] = v / total
    return dic


def dict_divide(dic: dict, divider):
    for k, v in dic.items():
        dic[k] = v / divider
    return dic


def dict_inverse(dic: dict):
    for k, v in dic.items():
        dic[k] = 1 / v
    return dic


def dict_max(dic_list):
    result = {}
    for dic in dic_list:
        for word, count in dic.items():
            if word not in result:
                result[word] = []
            result[word].append(count)

    for word, count_list in dict(result).items():
        result[word] = max(count_list)

    return result


def dict_sort(dic: dict, desc=False):
    sort = sorted(dic.items(), key=lambda x: x[1], reverse=desc)
    result = dict(sort)

    return result
