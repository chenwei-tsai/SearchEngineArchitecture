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

    def initialize(self, port, doc_server_id, document_pickle):
        self.port = port
        self.doc_server_id = doc_server_id
        self.docs = document_pickle

    @gen.coroutine
    def get(self, *args, **kwargs):
        print('[document server %d] is handling doc request' % self.doc_server_id)
        doc_id = self.get_query_argument("doc_id", None)
        try:
            doc_id = int(doc_id)
        except ValueError:
            self.write({"results": []})
            return
        if doc_id is None:
            self.write({"results": []})
            return
        if doc_id not in self.docs:
            self.write({"results": []})
            return
        response = dict()
        response['title'] = self.docs[doc_id]['title']
        response['url'] = self.docs[doc_id]['url']
        response['time'] = self.docs[doc_id]['date']
        response['source'] = self.docs[doc_id]['source']
        document_list = [response]
        return_map = {"results": document_list}
        self.write(json.dumps(return_map))


class UpdateHandler(web.RequestHandler):

    def initialize(self, port, doc_server_id):
        self.port = port
        self.doc_server_id = doc_server_id

    @gen.coroutine
    # def get(self):
    def get(self, *args, **kwargs):
        password = self.get_query_argument("p", None)
        if (password is None) or (password != UPDATE_PASSWORD):
            return
        load_document_pickle(self.doc_server_id)


def load_document_pickle(doc_server_id):
    srv_dump_file = os.getcwd() + "/document_server/doc_dumps/doc-srv-%d.dump" % doc_server_id
    with open(srv_dump_file, 'rb') as fin:
        doc_pickle = pkl.load(fin)
    print('[document server %d] pickle loading finished' % doc_server_id)
    return doc_pickle


def main(port_num, doc_server_id):

    document_pickle = load_document_pickle(doc_server_id)

    app = web.Application([
        web.url(r"/doc", DocHandler, dict(port=port_num, doc_server_id=doc_server_id,
                                          document_pickle=document_pickle)),
        web.url(r"/update", UpdateHandler)
    ])
    app.listen(port_num)
    print("[document server %d] is listening on " % doc_server_id + str(port_num))
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    portnum = int(sys.argvp[1])
    main(portnum, 0)
