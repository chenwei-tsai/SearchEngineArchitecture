import sys, os, json
sys.path.append(os.getcwd() + "/../")
try:
    import cPickle as pkl
except: ImportError:
    import pickle as pkl
from tornado import ioloop, web
from config import conf


class IndexHandler(web.RequestHandler):

    def initialize(self, port):
        self.port = port
        srv_id = port % 10
        srv_dump_file = os.getcwd() + "/indexdumps/index-srv-%d.dump" % srv_id
        with open(srv_dump_file, 'rb') as fin:
            self.data = pkl.load(fin)

    def get(self, *args, **kwargs):
        q = self.get_query_argument("q", None)
        if q is None or q not in self.data:
            self.write(json.dumps({"postings": []}))
            return
        postings = self.data[q]
        self.write(json.dumps({"postings": postings}))

def start(portnum):
    app = web.Application([web.url(r"/index", IndexHandler, dict(port=portnum))])
    app.listen(portnum)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    portnum = int(sys.argv[1])
    start(portnum)
