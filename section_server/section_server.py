from tornado import ioloop, web
from tornado import gen
from inventory import UPDATE_PASSWORD
import sys, os, json
sys.path.append(os.getcwd() + "/../")
try:
    import cPickle as pkl
except ImportError:
    import pickle as pkl


class SectionHandler(web.RequestHandler):

    def initialize(self, port, section_server_id, section_pickle):
        self.port = port
        self.section_server_id = section_server_id
        self.data = section_pickle

    @gen.coroutine
    # def get(self):
    def get(self, *args, **kwargs):
        print('[section server %d] is handling section request' % self.section_server_id)
        section = self.get_query_argument("s", None)
        if section is None or section not in self.data:
            self.write(json.dumps({"postings": []}))
            return
        postings = self.data[section]
        self.write(json.dumps({"postings": postings}))


class UpdateHandler(web.RequestHandler):

    def initialize(self, port, section_server_id):
        self.port = port
        self.section_server_id = section_server_id

    @gen.coroutine
    # def get(self):
    def get(self, *args, **kwargs):
        password = self.get_query_argument("p", None)
        if (password is None) or (password != UPDATE_PASSWORD):
            return
        load_section_pickle(self.section_server_id)


def load_section_pickle(section_server_id):
    srv_dump_file = os.getcwd() + "/section_server/section_dumps/section-srv-%d.dump" % section_server_id
    with open(srv_dump_file, 'rb') as fin:
        section_pickle = pkl.load(fin)
    print('[section server %d] pickle loading finished' % section_server_id)
    return section_pickle


def main(port_num, section_server_id):
    section_pickle = load_section_pickle(section_server_id)

    app = web.Application([
        web.url(r"/section", SectionHandler, dict(port=port_num, section_server_id=section_server_id,
                                                  section_pickle=section_pickle)),
        web.url(r"/update", UpdateHandler)
    ])

    app.listen(port_num)
    print("[section server %d] is listening on " % section_server_id + str(port_num))
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    port_num = int(sys.argv[1])
    main(port_num, 0)
