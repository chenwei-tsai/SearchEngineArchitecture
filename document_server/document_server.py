import sys, json, os
from tornado import ioloop
from tornado import web
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl

sys.path.append(os.getcwd() + "/../")


class DocHandler(web.RequestHandler):

    def initialize(self, port, doc_server_id):
        self.port = port
        DUMP_DIR = os.getcwd() + "/document_server/doc_dumps/"
        srv_id = doc_server_id
        srv_dump_file = DUMP_DIR + "doc-srv-%d.dump" % srv_id
        with open(srv_dump_file, 'rb') as fin:
            self.docs = pkl.load(fin)

    def get(self, *args, **kwargs):
        doc_id = self.get_query_argument("doc_id", None)
        try:
            doc_id = int(doc_id)
        except ValueError:
            self.write('illegal argument')
            return
        if doc_id is None:
            self.write({"results": []})
            return
        if doc_id not in self.docs:
            self.write("doc_id not in this server")
            return
        response = dict()
        response['title'] = self.docs[doc_id]['title']
        response['url'] = self.docs[doc_id]['url']
        response['date'] = self.docs[doc_id]['date']
        response['source'] = self.docs[doc_id]['source']
        document_List = [response]
        return_map = {"results": document_List}
        self.write(json.dumps(return_map))


def main(port_num, doc_server_id):
    app = web.Application([web.url(r"/doc", DocHandler, dict(port=port_num, doc_server_id=doc_server_id))])
    app.listen(port_num)
    print("[document server] is listening on " + str(port_num))
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    portnum = int(sys.argvp[1])
    main(portnum, 0)
