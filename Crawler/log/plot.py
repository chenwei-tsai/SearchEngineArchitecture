import cPickle as pkl
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import os, sys

files = os.listdir(os.getcwd())

for f in files:

    if not f.endswith('.pkl'):

        continue

    cls = f.split('_')[0]

    print("Plotting %s" % cls)

    data = pkl.load(open(f, "rb"))
    num = 30
    # print(data[0][2:2+num])

    words = []
    scores = []
    for i in range(2, 2+num):
        word = data[1][data[0][i][0]].encode("utf-8")
        score = data[0][i][1]
        scores.append(score)
        words.append(word)

    fig, ax = plt.subplots()
    y_pos = np.arange(len(words))

    x_scores = np.array(scores)
    perf = 10 * x_scores
    ax.barh(y_pos, perf, xerr=x_scores, align='center', color='blue', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words)
    ax.invert_yaxis()
    ax.set_xlabel('tf-idf score')
    ax.set_title("Class %s" % cls)

    plt.savefig(os.getcwd() + '/%s_tf_idf.png' % cls)

# print(data)


