from tornado import gen
from inventory import UPDATE_PASSWORD
import sys, json, os
from tornado import ioloop
from tornado import web
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl

sys.path.append(os.getcwd() + "/../")


class DocHandler(web.RequestHandler):

    def initialize(self, port, doc_server_id, docs):
        self.port = port
        self.doc_server_id = doc_server_id
        # self.init = init
        # self.docs = document_pickle
        self.docs = docs
        # print(self.docs["data"])


    @gen.coroutine
    def get(self, *args, **kwargs):
        print('[document server %d] is handling doc request' % self.doc_server_id)
        doc_id = self.get_query_argument("doc_id", None)
        update = self.get_query_argument("update", None)
        password = self.get_query_argument("p", None)

        # self.data["data"] = "doc not first"

        if update is not None and int(update) == 1:
            if password is None or password != UPDATE_PASSWORD:
                self.write(json.dumps({"results": "Forbidden access"}))
                return
            self.docs["data"] = load_document_pickle(self.doc_server_id)
            print("Doc server data updated")
            self.write(json.dumps({"results": "success"}))
            return

        try:
            doc_id = int(doc_id)
        except ValueError:
            self.write(json.dumps({"results": []}))
            return
        if doc_id is None:
            self.write(json.dumps({"results": []}))
            return
        if doc_id not in self.docs:
            self.write(json.dumps({"results": []}))
            return
        response = dict()
        response['title'] = self.docs["data"][doc_id]['title']
        response['url'] = self.docs["data"][doc_id]['url']
        response['time'] = self.docs["data"][doc_id]['date']
        response['source'] = self.docs["data"][doc_id]['source']
        document_list = [response]
        # document_list = []
        return_map = {"results": document_list}
        self.write(json.dumps(return_map))


# class UpdateHandler(web.RequestHandler):
#
#     def initialize(self, port, doc_server_id):
#         self.port = port
#         self.doc_server_id = doc_server_id
#
#     @gen.coroutine
#     # def get(self):
#     def get(self, *args, **kwargs):
#         password = self.get_query_argument("p", None)
#         if (password is None) or (password != UPDATE_PASSWORD):
#             return
#         load_document_pickle(self.doc_server_id)


def load_document_pickle(doc_server_id):
    srv_dump_file = os.getcwd() + "/document_server/doc_dumps/doc-srv-%d.dump" % doc_server_id
    with open(srv_dump_file, 'rb') as fin:
        doc_pickle = pkl.load(fin)
    print('[document server %d] pickle loading finished' % doc_server_id)
    return doc_pickle


def main(port_num, doc_server_id):

    document_pickle = load_document_pickle(doc_server_id)

    passdocs = dict()
    passdocs["data"] = document_pickle

    app = web.Application([
        web.url(r"/doc", DocHandler, dict(port=port_num, doc_server_id=doc_server_id,
                                          docs=passdocs)),
        # web.url(r"/update", UpdateHandler)
    ])
    app.listen(port_num)
    print("[document server %d] is listening on " % doc_server_id + str(port_num))
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    portnum = int(sys.argvp[1])
    main(portnum, 0)
