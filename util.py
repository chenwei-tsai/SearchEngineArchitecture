import string
import re
import datetime

def datetime_diff(datetime_object):
    now_object = datetime.datetime.now()
    delta = now_object - datetime_object
    if delta.days < 1:
        minutes = int(delta.seconds / 60)
        if minutes < 60:
            return str(int(delta.seconds / 60)) + ' mins ago'
        else:
            return str(int(minutes / 60)) + ' hours ago'
    else:
        return str(delta.days) + ' days ago'


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
    # if cat == "art":
    #     return 0
    if cat == "sport":
        return 0
    elif cat == "business":
        return 1
    elif cat == "tech":
        return 2
    elif cat == "entertain":
        return 3
    elif cat == "opinion":
        return 4
    elif cat == "world":
        return 5
    elif cat == "us":
        return 6
    else:
        return -1

def label_to_category(cat):
    # if cat == "0":
    #     return "art"
    if cat == 0:
        return "sport"
    elif cat == 1:
        return "business"
    elif cat == 2:
        return "tech"
    elif cat == 3:
        return "entertain"
    elif cat == 4:
        return "opinion"
    elif cat == 5:
        return "world"
    elif cat == 6:
        return "us"
    else:
        return "ERROR"

DATE_TO_NUM = {'Jan': "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

def get_time(time):

    if ',' in time:
        date = time.split(',')[0].strip().split(' ')
        seconds = time.split(',')[1].strip().split(' ')

        if len(date[1]) == 1:
            date[1] = '0' + date[1]

        fmt_date = date[2] + DATE_TO_NUM[date[0]] + date[1]
        if seconds[1] == 'pm':
            fmt_seconds = str(int(seconds[0].split(':')[0]) + 12) + seconds[0].split(':')[1]
        else:
            fmt_seconds = "".join(seconds[0].split(':'))
        if len(fmt_seconds) == 3:
            fmt_seconds = '0' + fmt_seconds
        out_time = fmt_date + fmt_seconds
    else:
        fmt_date = "".join(time.split("T")[0].strip().split('-'))
        fmt_seconds = "".join(time.split("T")[1].strip().split('-')[0].split(':')[0:2])
        out_time = fmt_date + fmt_seconds
    return out_time

