import re


def unicode_char_cleaner(text, replacement=" "):
    text = re.sub(r"\\[ux][a-z0-9A-Z]+", replacement, text)
    text = re.sub(r"[\\]{1,2}[a-z0-9A-Z]{1}", replacement, text)
    return text


if __name__ == "__main__":
    print('ok')
    print(unicode_char_cleaner("Manoj,\\\\n\\\\nPlease"))
    print(unicode_char_cleaner("Hi \\xc3\\xe0\\u0159Y\\xe3\\u0144 \\xe9\\u0165\\u0165r\\u012f! Thanks"))
