import pickle as pkl
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
import numpy as np

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

if __name__ == "__main__":
    trdata_file = 'trdata.pkl'
    tedata_file = 'tedata.pkl'
    features_file = 'features.pkl'

    trdata = pkl.load(open(trdata_file))
    tedata = pkl.load(open(tedata_file))
    features = pkl.load(open(features_file))

    tr_data = trdata[0]
    tr_labels = trdata[1]
    te_data = tedata[0]
    te_labels = tedata[1]
    assert(len(tr_data) == len(tr_labels))
    assert(len(te_data) == len(te_labels))

    print("Training data size: {}".format(len(tr_data)))
    X_train = encoding(tr_data, features)
    Y_train = np.array(tr_labels)

    X_test = encoding(te_data, features)
    Y_test = np.array(te_labels)

    assert(len(X_train) == len(Y_train))
    assert(len(X_test) == len(Y_test))

    classifier = MultinomialNB()
    # classifier = BernoulliNB()

    model = classifier.fit(X_train, Y_train)

    probs = model.predict_proba(X_train).tolist()

    err = 0.0
    for i, prob in enumerate(probs):
        Y_pred = np.argmax(prob)
        # print "Label:{}, Predict:{}".format(Y_train[i], Y_pred)
        if Y_train[i] != Y_pred:
            err = err + 1

    print("Training error: %.4f" % (err/len(X_train)))

    test_probs = model.predict_proba(X_test).tolist()

    err = 0.0
    for i, test_probs in enumerate(test_probs):
        Y_pred = np.argmax(test_probs)
        # print "Label:{}, Predict:{}".format(Y_test[i], Y_pred)
        if Y_test[i] != Y_pred:
            err = err + 1

    print("Training error: %.4f" % (err/len(X_test)))




