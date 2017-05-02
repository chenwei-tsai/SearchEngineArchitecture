import sys, os, json
sys.path.append(os.getcwd() + "/../")
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl
from tornado import ioloop, web
from tornado import gen
from config import conf


class SectionHandler(web.RequestHandler):

    def initialize(self, port, section_server_id):
        self.port = port
        srv_id = section_server_id
        srv_dump_file = os.getcwd() + "/section_server/section_dumps/section-srv-%d.dump" % srv_id
        with open(srv_dump_file, 'rb') as fin:
            self.data = pkl.load(fin)
        # print('section server loading finished')

    @gen.coroutine
    # def get(self):
    def get(self, *args, **kwargs):
        # print('section server handling request')
        section = self.get_query_argument("s", None)
        if section is None or section not in self.data:
            self.write(json.dumps({"postings": []}))
            return
        postings = self.data[section]
        self.write(json.dumps({"postings": postings}))


def main(port_num, section_server_id):
    app = web.Application([web.url(r"/section", SectionHandler, dict(port=port_num, section_server_id=section_server_id))])
    app.listen(port_num)
    print("[section server] is listening on " + str(port_num))
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    port_num = int(sys.argv[1])
    main(port_num, 0)
