import os
import json
import numpy as np

DIR = os.getcwd()
DOC_DIR = DIR + '/crawled_document'

list_files = os.listdir(DOC_DIR)

trsize = 0
tesize = 0

for f in list_files:
    if not f.endswith(".txt"):
        continue
    # with open(DOC_DIR + '/' + f) as fin:
        # text = json.load(fin)
        # target = text['section'].encode("utf-8").replace("\xe2\x80\x99", "'")
    a = np.random.uniform()
    if a <= 0.85:
        os.system("mv {} {}".format(DOC_DIR+'/'+f, DOC_DIR+'/'+'training'))
        trsize = trsize + 1
    else:
        os.system("mv {} {}".format(DOC_DIR+'/'+f, DOC_DIR+'/'+'testing'))
        tesize = tesize + 1

print("--------------------")
print("Training data: {}".format(trsize))
print("Testing data: {}".format(tesize))
