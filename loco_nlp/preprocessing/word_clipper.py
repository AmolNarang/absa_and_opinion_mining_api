

def clip(text):
    def clipper(input_text):
        tokens = input_text.split()
        if len(tokens) > 250:
            tokens = tokens[:250]
        return ' '.join(tokens)
    return list(map(clipper, text)) if type(text) is list else clipper(text)


if __name__ == "__main__":
    print("ok")
    print(clip("jksdnn skdlngvlksdn sdnffklsdn sister couldn, t attend Jeff's party because she didn't study."))
    print(clip(["jksdnn skdlngvlksdn sdnffklsdn sister couldn, t attend Jeff's party because she didn't study."]))