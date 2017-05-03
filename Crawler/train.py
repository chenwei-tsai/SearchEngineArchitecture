import pickle as pkl
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn import svm
import numpy as np
import os, sys
sys.path.append(os.getcwd() + "/../")
from util import label_to_category

SAVE_MODEL = False

def encoding(data, features):
    result = []

    for x in data:
        x = set(x)
        temp = []
        for word in features:
            if word in x:
                temp.append(1)
            else:
                temp.append(0)
        temp = np.array(temp)
        result.append(temp)
    return result


def naive_bayes(X_train, Y_train, X_test, Y_test):

    print("-------------Start training: Naive Bayes--------------")

    classifier = MultinomialNB()

    model = classifier.fit(X_train, Y_train)

    if SAVE_MODEL:
        DIR = os.getcwd()
        model_file = DIR + "/../model/nb-model-03.model"
        pkl.dump(model, open(model_file, 'wb'))

    probs = model.predict_proba(X_train).tolist()

    err = 0.0
    err_by_class = dict()
    for i, prob in enumerate(probs):
        cls = label_to_category(Y_train[i])
        if cls not in err_by_class:
            err_by_class[cls] = {}
            err_by_class[cls]['err'] = 0.0
            err_by_class[cls]['count'] = 0.0
        Y_pred = np.argmax(prob)
        err_by_class[cls]['count'] = err_by_class[cls]['count'] + 1
        if Y_train[i] != Y_pred:
            err = err + 1
            err_by_class[cls]['err'] = err_by_class[cls]['err'] + 1

    print("Training err: %.4f" % (err/len(X_train)))
    for cls in err_by_class:
        print("Class %s, all: %f, err: %f, test error: %.4f" % (cls, err_by_class[cls]['count'], err_by_class[cls]['err'], err_by_class[cls]['err']/err_by_class[cls]['count']))


    test_probs = model.predict_proba(X_test).tolist()

    err = 0.0
    for i, test_probs in enumerate(test_probs):
        Y_pred = np.argmax(test_probs)
        # print "Label:{}, Predict:{}".format(Y_test[i], Y_pred)
        if Y_test[i] != Y_pred:
            err = err + 1


    print("Testing error: %.4f" % (err/len(X_test)))

def linear_svm(X_train, Y_train, X_test, Y_test):

    print("-------------Start training: SVM--------------")

    clf = svm.SVC(probability=True)
    clf.fit(X_train, Y_train)

    probs = clf.predict_proba(X_train)

    err = 0.0
    for i, prob in enumerate(probs):
        lbl = np.argmax(prob)
        if Y_train[i] != lbl:
            err = err + 1
    print("Training err: %.4f" % (err/len(X_train)))

    test_probs = clf.predict_proba(X_test)

    err = 0.0
    for i, prob in enumerate(test_probs):
        lbl = np.argmax(prob)
        if Y_test[i] != lbl:
            err = err + 1
    print("Testing err: %.4f" % (err/len(X_test)))

if __name__ == "__main__":
    trdata_file = './dataset/trdata.pkl'
    tedata_file = './dataset/tedata.pkl'
    features_file = './dataset/features.pkl'

    print("-------------Read data--------------")
    trdata = pkl.load(open(trdata_file))
    tedata = pkl.load(open(tedata_file))
    features = pkl.load(open(features_file))

    tr_data = trdata[0]
    tr_labels = trdata[1]
    te_data = tedata[0]
    te_labels = tedata[1]
    assert(len(tr_data) == len(tr_labels))
    assert(len(te_data) == len(te_labels))

    print("Feature size: {}".format(len(features)))
    print("Training data size: {}".format(len(tr_data)))
    print("Test data size: {}".format(len(te_data)))
    X_train = encoding(tr_data, features)
    Y_train = np.array(tr_labels)

    X_test = encoding(te_data, features)
    Y_test = np.array(te_labels)

    assert(len(X_train) == len(Y_train))
    assert(len(X_test) == len(Y_test))

    naive_bayes(X_train, Y_train, X_test, Y_test)
    # linear_svm(X_train, Y_train, X_test, Y_test)

