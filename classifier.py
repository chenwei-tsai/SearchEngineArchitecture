import os, argparse, json, sys
from util import unicode_to_ascii, tokenize, label_to_category
import numpy as np
from config import conf
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl


DIR = os.getcwd()
model_file = DIR + "/nb-model-02.model"
features_file = DIR + "/features.pkl"


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

def classify(f_dir):

    model = pkl.load(open(model_file, 'rb'))
    features = pkl.load(open(features_file, 'rb'))

    outputs = list()

    files = os.listdir(DIR + "/" + f_dir)

    for f in files:
        output = dict()
        traindata = list()

        with open(DIR + "/" + f_dir + "/" + f) as fin:
            text = json.load(fin)
            output["title"] = unicode_to_ascii(text["title"].encode("utf-8"))
            output["date"] = unicode_to_ascii(text["created_date"].encode("utf-8"))
            output["url"] = unicode_to_ascii(text["url"].encode("utf-8"))
            output["source"] = unicode_to_ascii(text["source"].encode("utf-8"))
            output["date"] = unicode_to_ascii(text["updated_date"].encode("utf-8"))
            content = tokenize(unicode_to_ascii(text["text"].encode("utf-8")))
            if content is None or len(content) == 0:
                print("File %s has no text" % f)
                continue
            traindata.append(content)
        X_arr = encoding(traindata, features)
        probs = model.predict_proba(X_arr).tolist()
        Y = np.argmax(probs[0])

        output["category"] = label_to_category(Y)
        output["score"] = probs[0][Y]
        outputs.append(output)

    return outputs

def dump_to_servers(outputs):

    MAX_DOC_ID = 0

    num_doc_srvs = len(conf["DOC_SERVERS"])
    num_idx_srvs = len(conf["INDEX_SERVERS"])
    doc_srv_data = list(dict())
    idx_srv_data = list(dict())
    doc_srv_file_paths = list()
    idx_srv_file_paths = list()

    for i in range(0, num_doc_srvs):
        srv_dump_file = os.getcwd() + "/" + conf["DOC_SRV_DIR"] + "/doc-srv-%d.dump" % i
        doc_srv_file_paths.append(srv_dump_file)
        if os.path.exists(srv_dump_file):
            docs = pkl.load(open(srv_dump_file, "rb"))
        else:
            docs = {}
        doc_srv_data.append(docs)

    for i in range(0, num_idx_srvs):
        srv_dump_file = os.getcwd() + "/" + conf["INDEX_SRV_DIR"] + "/index-srv-%d.dump" % i
        idx_srv_file_paths.append(srv_dump_file)
        if os.path.exists(srv_dump_file):
            docs = pkl.load(open(srv_dump_file, "rb"))
        else:
            docs = {}
        idx_srv_data.append(docs)


    for output in outputs:
        print("--------------------------------")
        print("Title: %s" % output["title"])
        print("Date: %s" % output["date"])
        print("Topic: %s" % output["category"])

        topic = output["category"]

        doc_id = MAX_DOC_ID + 1
        MAX_DOC_ID = MAX_DOC_ID + 1
        doc_srv_id = doc_id % len(conf["DOC_SERVERS"])
        idx_srv_id = hash(topic) % len(conf["INDEX_SERVERS"])

        print("Dump doc_id: {}, topic: {} to docserver {}, index server {}".format(doc_id, output["category"], doc_srv_id, idx_srv_id))
        doc_srv_data[doc_srv_id][doc_id] = output
        if topic not in idx_srv_data[idx_srv_id]:
            idx_srv_data[idx_srv_id][topic] = []
        idx_srv_data[idx_srv_id][topic].append((doc_id, output["score"]))

    for i, file_path in enumerate(doc_srv_file_paths):
        pkl.dump(doc_srv_data[i], open(file_path, 'wb'))

    for i, file_path in enumerate(idx_srv_file_paths):
        pkl.dump(idx_srv_data[i], open(file_path, 'wb'))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_dir_path", required=True)

    args = parser.parse_args()

    outputs = classify(args.file_dir_path)

    dump_to_servers(outputs)

