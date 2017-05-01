import sys, json, os
sys.path.append(os.getcwd() + "/../")
from tornado import ioloop, web
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl

class DocHandler(web.RequestHandler):

    def initialize(self, port):
        self.port = port
        DUMP_DIR = os.getcwd() + "/docdumps/"
        srv_id = port % 3
        srv_dump_file = DUMP_DIR + "doc-srv-%d.dump" % srv_id + srv_id
        with open(srv_dump_file, 'rb') as fin:
            self.docs = pkl.load(fin)

    def get(self, *args, **kwargs):
        doc_id = self.get_query_argument("doc_id", None)
        if doc_id is None:
            self.write({"results": []})
            return
        if doc_id not in self.docs:
            self.write({"doc_id not in this server"})
            return
        response = dict()
        response['title'] = self.docs[doc_id]['title']
        response['url'] = self.docs[doc_id]['url']
        response['date'] = self.docs[doc_id]['date']
        response['source'] = self.docs[doc_id]['source']

        self.write(json.dumps(response))

def start(portnum):
    app = web.Application([web.url(r"/doc", DocHandler, dict(port=portnum))])
    app.listen(portnum)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    portnum = int(sys.argvp[1])
    start(portnum)
