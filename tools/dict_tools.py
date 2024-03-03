def dict_merger(master: dict, slave: dict):
    base = slave
    for k, v in master.items():
        if type(v) is dict:
            base[k] = dict_merger(v, base.get(k, {}))
        elif type(v) is list and (k in slave and type(slave[k]) is list):
            for i in v:
                if i not in base[k]:
                    base[k].append(i)
        else:
            base[k] = v

    return base


def max_in_dict(dic):
    val = 0
    result = None
    for k, v in dic.items():
        if v >= val:
            val = v
            result = k
    return result


def dict_multiply(dic: dict, number):
    for k in dic.keys():
        dic[k] *= number
    return dic


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


def dict_and(dict1: dict, dict2: dict):
    return {i: dict1[i] and dict2[j] for i, j in zip(dict1.keys(), dict2.keys())}


def dict_or(dict1: dict, dict2: dict):
    return {i: dict1[i] and dict2[j] for i, j in zip(dict1.keys(), dict2.keys())}


def dict_not(dict1: dict, dict2: dict):
    return {i: not(dict1[i] and dict2[j]) for i, j in zip(dict1.keys(), dict2.keys())}


if __name__ == "__main__":
    print(dict_merger(
        {"a": [1, 2, 4], "b": {'a': 10}, "e": [1, 5, 3]},
        {'c': "dskfj", "d": None, "b": {"c": 20}, "x": [4, 5, 6]}))

    print(dict_softmax({1: 5, 2: 5, 3: 10}))
    print(dict_sum({1: 0, 2: 2, 3: 3}, {1: 2, 100: 4, 2: 10}))
