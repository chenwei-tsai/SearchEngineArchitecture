import os
import json
import sys
import pickle
import numpy as np
from util import unicode_to_ascii, tokenize, category_to_label, label_to_category
from sklearn.feature_extraction.text import TfidfVectorizer

DIR = os.getcwd()

TR_DOC_DIR = DIR + '/crawled_document/training'
tr_list_files = os.listdir(TR_DOC_DIR)
TE_DOC_DIR = DIR + '/crawled_document/testing'
te_list_files = os.listdir(TE_DOC_DIR)

LOG_DIR = DIR + '/log'


art = ["Arts", "Theater", "Movies", "Books", "Multimedia/Photos"]
sport = ["Well", "Sports", "Automobiles"]
business = ["Job Market", "Your Money", "Business Day", "Real Estate"]
tech = ["Science", "Technology"]
entertain = ["Food", "Travel", "Watching", "Crosswords & Games", "Podcasts", "Magazine", "T Magazine", "Style", "Fashion & Style"]
opinion = ["Opinion"]
world = ["World"]
us = ["U.S."]

classes = ["art", "sport", "business", "tech", "entertain", "opinion", "world", "us"]

# WORD_DICT = set()

CORPUS = dict(list())

def readData():

    trcount = dict()
    tecount = dict()

    trdata = list()
    trlabel = list()
    tedata = list()
    telabel = list()

    for f in tr_list_files:
        if not f.endswith(".txt"):
            continue
        with open(TR_DOC_DIR + '/' + f) as fin:
            text = json.load(fin)
            target = text['section'].encode("utf-8").replace("\xe2\x80\x99", "'")
            if target in art:
                target = 'art'
            elif target in sport:
                target = 'sport'
            elif target in business:
                target = 'business'
            elif target in tech:
                target = 'tech'
            elif target in entertain:
                target = 'entertain'
            elif target in opinion:
                target = 'opinion'
            elif target in world:
                target = 'world'
            elif target in us:
                target = 'us'
            else:
                continue
            if target not in trcount:
                trcount[target] = 0
            trcount[target] = trcount[target] + 1

            label = category_to_label(target)
            content = tokenize(unicode_to_ascii(text['text'].encode('utf-8')))

            if target not in CORPUS:
                CORPUS[target] = []
            CORPUS[target].append(" ".join(content))
            # for word in content:
            #     WORD_DICT.add(word)
            trdata.append(content)
            trlabel.append(label)

    for f in te_list_files:
        if not f.endswith(".txt"):
            continue
        with open(TE_DOC_DIR + '/' + f) as fin:
            text = json.load(fin)
            target = text['section'].encode("utf-8").replace("\xe2\x80\x99", "'")
            if target in art:
                target = 'art'
            elif target in sport:
                target = 'sport'
            elif target in business:
                target = 'business'
            elif target in tech:
                target = 'tech'
            elif target in entertain:
                target = 'entertain'
            elif target in opinion:
                target = 'opinion'
            elif target in world:
                target = 'world'
            elif target in us:
                target = 'us'
            else:
                continue
            if target not in tecount:
                tecount[target] = 0
            tecount[target] = tecount[target] + 1

            label = category_to_label(target)
            content = tokenize(unicode_to_ascii(text['text'].encode('utf-8')))
            # for word in content:
            #     WORD_DICT.add(word)

            tedata.append(content)
            telabel.append(label)

    print("------Training data------")
    print(trcount)
    print("------Testing data------")
    print(tecount)
    # print(CORPUS['sport'])
    return trdata, trlabel, tedata, telabel

def encoding(data, label, feature_set):

    print("class {}".format(label_to_category(label)))

    newdata = data

    for pair in zip(data, data[1:]):
        newdata.append(" ".join(pair))

    newdata = set(newdata)
    arr = []
    for feature in feature_set:
        if feature in newdata:
            arr.append(1)
        else:
            arr.append(0)

    for i, word in enumerate(feature_set):
        print ("{}: {}".format(word, arr[i]))


if __name__ == "__main__":

    trdata, trlabel, tedata, telabel = readData()

    feature_set = set()

    for c in classes:
        print("Adding features from class {}".format(c))
        tfidf = TfidfVectorizer(analyzer='word', ngram_range = range(1, 3), min_df=0, stop_words='english')
        matrix = tfidf.fit_transform(CORPUS[c])
        feature_names = tfidf.get_feature_names()

        dense = matrix.todense()
        dense_mean = dense.mean(axis=0)

        l = dense_mean.tolist()[0]

        scores = [pair for pair in zip(range(0, len(l)), l) if pair[1] > 0]
        scores = sorted(scores, key = lambda x : x[1], reverse=True)

        log_file = LOG_DIR + '/' + c + "_tfidf_dist.pkl"
        outfile = open(log_file, 'wb')
        pickle.dump((scores, feature_names), outfile)

        for word, score in [(feature_names[i], s) for (i, s) in scores[:50]]:
            # print("{}: {}".format(word, score))
            feature_set.add(word.encode("utf-8"))

    feature_set.remove("mr")
    feature_set.remove("ms")
    feature_set.remove("said")

    print(feature_set)

    trdata_file = DIR + '/' + 'trdata.pkl'
    tedata_file = DIR + '/' + 'tedata.pkl'
    if not os.path.exists(trdata_file):
        pickle.dump(feature_set, open(feature_file, 'wb'))
    if not os.path.exists(tedata_file):
        pickle.dump((trdata, trlabel), open(trdata_file, 'wb'))


    # feature_file = DIR + '/' + 'features.pkl'
    # pickle.dump((tedata, telabel), open(tedata_file, 'wb'))

    # encoding(trdata[200], trlabel[200], feature_set)







