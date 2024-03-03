from loco_nlp.config import CONJUNCTIONS


def detect_conjunctions(text):
    def detector(input_text):
        try:
            result = []
            for word in CONJUNCTIONS:
                if word in input_text:
                    result.append(word)

            return result

        except:
            return []

    return list(map(detector, text)) if type(text) is list else detector(text)


if __name__ == "__main__":
    print("ok")
    print(detect_conjunctions('HDFC Bank is better bank than Yes Bank'))
    print(detect_conjunctions(['HDFC Bank is better bank than Yes Bank and AU Bank', 'The Mo .bile is good but battery sucks', '']))