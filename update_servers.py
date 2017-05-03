import os, json, sys, time
DIR = os.getcwd()
sys.path.append(DIR + "/model")
from tornado import ioloop, httpclient, gen
from inventory import CRAWLER_DOC_DIRS, CRAWLER_DUMP_DIRS, servers, UPDATE_PASSWORD
from classifier import start_classify

try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl


@gen.coroutine
def main():

    while True:
        print("Start check crawler updates")
        isUpdate = False
        for source, rel_dir in CRAWLER_DOC_DIRS.items():
            doc_dir = DIR + rel_dir
            print("Check updates from source {}, dir {}".format(source, doc_dir))
            files = os.listdir(doc_dir)
            if files is None or len(files) == 0:
                print("No updates from source {}".format(source))
                continue

            isUpdate = True
            # dump new collected docs to servers
            # start_classify(doc_dir, source)
            start_classify(doc_dir)

            # Clean dumped data
            doc_dump_dir = DIR + CRAWLER_DUMP_DIRS[source]
            for f in files:
                os.system('mv {} {}'.format(doc_dir+'/'+f, doc_dump_dir))

            rest_files = os.listdir(doc_dir)
            # assert(rest_files is None or len(rest_files) == 0)

        if isUpdate:
            print("Server need to update")
            http_client = httpclient.AsyncHTTPClient()
            for sec_srv in servers["section_server"]:
                query_url = sec_srv + "/section?update=1&p=%s" % UPDATE_PASSWORD
                response = yield http_client.fetch(query_url)
                raw_data = json.loads(response.body.decode('utf-8'))
                if raw_data["postings"] == "success":
                    print("Server %s successfully updates" % sec_srv)
                else:
                    print("Server %s failed updating" % sec_srv)
                    print(raw_data["postings"])
                    exit(1)

            for doc_srv in servers["document_server"]:
                query_url = doc_srv + "/doc?update=1&p=%s" % UPDATE_PASSWORD
                response = yield http_client.fetch(query_url)
                raw_data = json.loads(response.body.decode("utf-8"))
                if raw_data["results"] == "success":
                    print("Server %s successfully updates" % doc_srv)
                else:
                    print("Server %s failed updating" % doc_srv)
                    print(raw_data["results"])
                    exit(1)

        print("Update ended")
        try:
            print("Sleep..........................")
            time.sleep(60 * 1)
        except:
            print('update sleep interrupted')


if __name__ == "__main__":
    ioloop.IOLoop.instance().run_sync(main)
