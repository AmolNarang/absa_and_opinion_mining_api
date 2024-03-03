import random

import pandas as pd
from fuzzywuzzy import fuzz


class TextGrouper:

    def __init__(self, input_list, output_format, clip_range=5, length_ratio=0.4):
        self.input_list = input_list
        self.output_format = output_format
        self.clip_range = clip_range
        self.length_ratio = length_ratio
        self.clipped_list = []
        self.similar_sentence = {}

    def random_clip(self, input_string):
        n = len(input_string)
        for i in range(0, self.clip_range):
            rand_range = random.randint(0, int(n*(1-self.length_ratio)))
            self.clipped_list.append(input_string[rand_range:rand_range+int(n*self.length_ratio)])
        return self.clipped_list

    def compare_row(self, clipped_text, row_text, original_text):
        for t in clipped_text:
            if t in row_text:
                score = fuzz.ratio(row_text, original_text)
                if score > 70:
                    return True
                else:
                    return False
        return False

    def perform_grouping(self):
        visited_index = {}
        for i1_, resp1 in enumerate(self.input_list):
            if i1_ in visited_index:
                continue
            else:
                visited_index[i1_] = 1

            clipped_text = self.random_clip(resp1)
            for i2_, resp2 in enumerate(self.input_list):
                if i2_ in visited_index:
                    continue
                if self.compare_row(clipped_text, resp2, resp1):
                    visited_index[i2_] = 1

                    if i1_ not in self.similar_sentence:
                        self.similar_sentence[i1_] = [i2_]
                    else:
                        self.similar_sentence[i1_].append(i2_)

        possible_canned_keys = sorted(self.similar_sentence, key=lambda k: len(self.similar_sentence[k]), reverse=True)
        possible_canned_r = [{i: self.similar_sentence[i]} for i in possible_canned_keys]

        if self.output_format.lower() == "key":
            print(len(possible_canned_r))
            return possible_canned_r

        elif self.output_format.lower() == "value":
            res_dict = {}
            for d in possible_canned_r:
                for k, v in d.items():
                    res_dict.update({self.input_list[k]: [self.input_list[v1] for v1 in v]})
            print(len(res_dict))
            return res_dict

        else:
            print("Kindly specify output_format as (key or value) only")
            return None


if __name__ == "__main__":
    frmt_yb = pd.read_csv('/home/user/Projects/auto_suggestion_development/data/split_yes_bank.csv')
    ip_list = list(frmt_yb["Response"])[:100]
    g = TextGrouper(input_list=ip_list, output_format='value')
    x = g.perform_grouping()

    print(x)
