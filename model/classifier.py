import os, argparse, json, sys, hashlib, re
DIR = os.getcwd()
sys.path.append(DIR + "/../")
from util import unicode_to_ascii, tokenize, label_to_category, get_time
import numpy as np
# from config import conf
from inventory import MODEL_DIR, DOC_SRV_DIR, SEC_SRV_DIR, servers
# try:
#     import cPickle as pkl
# except ImportError:
import pickle as pkl



model_file = MODEL_DIR + "/nb-model-02.model"
features_file = MODEL_DIR + "/features.pkl"

def my_hash(s):
    return int(hashlib.md5(s).hexdigest()[:8], 16)

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

    files = os.listdir(f_dir)

    for f in files:
        output = dict()
        traindata = list()

        if not f.endswith(".txt"):
            continue

        with open(f_dir + "/" + f) as fin:
            text = json.load(fin)
            # if source == "NYT":
            output["title"] = unicode_to_ascii(text["title"].encode("utf-8"))
            output["date"] = get_time(unicode_to_ascii(text["time"].encode("utf-8")))
            output["url"] = unicode_to_ascii(text["url"].encode("utf-8"))
            output["source"] = unicode_to_ascii(text["source"].encode("utf-8"))
            # elif source == "FOX":
            #     output["title"] = unicode_to_ascii(text["title"].encode("utf-8"))
            #     output["date"] = get_time(unicode_to_ascii(text["time"].encode("utf-8")))
            #     output["url"] = unicode_to_ascii(text["url"].encode("utf-8"))
            #     output["source"] = source
            # else:
            #     output["title"] = unicode_to_ascii(text["title"].encode("utf-8"))
            #     output["date"] = get_time(unicode_to_ascii(text["tile"].encode("utf-8")))
            #     output["url"] = unicode_to_ascii(text["url"].encode("utf-8"))
            #     output["source"] = source
            content = tokenize(unicode_to_ascii(text["text"].encode("utf-8")))
            if content is None or len(content) == 0:
                print("File %s has no text" % f)
                continue

            raw_text = unicode_to_ascii(text["text"].encode("utf-8"))
            indexes = [i.start() for i in re.finditer(r"\.", raw_text)]
            if len(indexes) == 0:
                continue

            if len(indexes) <= 3:
                stop = len(indexes)-1
            else:
                stop = 3
            output["snippet"] = raw_text[0:indexes[stop]+1]

            traindata.append(content)

        X_arr = encoding(traindata, features)
        probs = model.predict_proba(X_arr).tolist()
        Y = np.argmax(probs[0])

        output["category"] = label_to_category(Y)
        output["score"] = probs[0][Y]
        outputs.append(output)

    return outputs

def dump_to_servers(outputs):


    # num_doc_srvs = len(conf["DOC_SERVERS"])
    num_doc_srvs = len(servers["document_server"])
    # num_idx_srvs = len(conf["SECTION_SERVERS"])
    num_idx_srvs = len(servers["section_server"])
    doc_srv_data = list(dict())
    idx_srv_data = list(dict())
    doc_srv_file_paths = list()
    idx_srv_file_paths = list()

    for i in range(0, num_doc_srvs):
        srv_dump_file = DOC_SRV_DIR + "/doc_dumps/doc-srv-%d.dump" % i
        doc_srv_file_paths.append(srv_dump_file)
        if os.path.exists(srv_dump_file):
            docs = pkl.load(open(srv_dump_file, "rb"))
        else:
            docs = {}
        doc_srv_data.append(docs)

    for i in range(0, num_idx_srvs):
        srv_dump_file = SEC_SRV_DIR + "/section_dumps/section-srv-%d.dump" % i
        idx_srv_file_paths.append(srv_dump_file)
        if os.path.exists(srv_dump_file):
            docs = pkl.load(open(srv_dump_file, "rb"))
        else:
            docs = {}
        idx_srv_data.append(docs)


    for output in outputs:
        # print("--------------------------------")
        # print("Title: %s" % output["title"])
        # print("Date: %s" % output["date"])
        # print("Topic: %s" % output["category"])

        topic = output["category"]

        # doc_id = MAX_DOC_ID + 1
        doc_id = my_hash(output['url'])
        doc_srv_id = doc_id % len(servers['document_server'])
        idx_srv_id = my_hash(topic) % len(servers['section_server'])

        doc_time = output["date"]

        if doc_id in doc_srv_data[doc_srv_id]:
            # print("Already in doc server, title: {}".format(output["title"]))
            continue

        # print("Dump doc_id: {}, topic: {} to docserver {}, section server {}".format(doc_id, output["category"], doc_srv_id, idx_srv_id))
        doc_srv_data[doc_srv_id][doc_id] = output
        if topic not in idx_srv_data[idx_srv_id]:
            idx_srv_data[idx_srv_id][topic] = []
        idx_srv_data[idx_srv_id][topic].append((doc_id, (output["score"], doc_time)))

    for i, file_path in enumerate(doc_srv_file_paths):
        pkl.dump(doc_srv_data[i], open(file_path, 'wb'))

    for i, file_path in enumerate(idx_srv_file_paths):
        pkl.dump(idx_srv_data[i], open(file_path, 'wb'))

def start_classify(file_path):

    outputs = classify(file_path)
    dump_to_servers(outputs)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_dir_path", required=True)
    args = parser.parse_args()

    start_classify(args.file_dir_path)

