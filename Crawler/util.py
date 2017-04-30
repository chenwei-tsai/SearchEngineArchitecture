import string, re

def unicode_to_ascii(text):
    TEXT = (text.
            replace('\xe2\x80\x99', "'").
            replace('\xc3\xa9', 'e').
            replace('\xe2\x80\x90', '-').
            replace('\xe2\x80\x91', '-').
            replace('\xe2\x80\x92', '-').
            replace('\xe2\x80\x93', '-').
            replace('\xe2\x80\x94', '-').
            replace('\xe2\x80\x94', '-').
            replace('\xe2\x80\x98', "'").
            replace('\xe2\x80\x9b', "'").
            replace('\xe2\x80\x9c', '"').
            replace('\xe2\x80\x9c', '"').
            replace('\xe2\x80\x9d', '"').
            replace('\xe2\x80\x9e', '"').
            replace('\xe2\x80\x9f', '"').
            replace('\xe2\x80\xa6', '...').#
            replace('\xe2\x80\xb2', "'").
            replace('\xe2\x80\xb3', "'").
            replace('\xe2\x80\xb4', "'").
            replace('\xe2\x80\xb5', "'").
            replace('\xe2\x80\xb6', "'").
            replace('\xe2\x80\xb7', "'").
            replace('\xe2\x81\xba', "+").
            replace('\xe2\x81\xbb', "-").
            replace('\xe2\x81\xbc', "=").
            replace('\xe2\x81\xbd', "(").
            replace('\xe2\x81\xbe', ")")
            )
    return TEXT

def tokenize(text):
    for punc in string.punctuation:
        if punc == "'":
            continue
        text = string.replace(text, punc, "")
    origin = re.findall("[\S]+", text)
    tokens = [w.lower() for w in origin]
    return tokens

def category_to_label(cat):
    if cat == "art":
        return 0
    elif cat == "sport":
        return 1
    elif cat == "business":
        return 2
    elif cat == "tech":
        return 3
    elif cat == "entertain":
        return 4
    elif cat == "opinion":
        return 5
    elif cat == "world":
        return 6
    elif cat == "us":
        return 7
    else:
        return -1

def label_to_category(cat):
    if cat == "0":
        return "art"
    elif cat == "1":
        return "sport"
    elif cat == 2:
        return "business"
    elif cat == 3:
        return "tech"
    elif cat == 4:
        return "entertain"
    elif cat == 5:
        return "opinion"
    elif cat == 6:
        return "world"
    elif cat == 7:
        return "us"
    else:
        return "ERROR"
