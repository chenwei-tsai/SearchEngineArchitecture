import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import operator
import hashlib

from inventory import DOCUMENT_SERVER_NUM
from inventory import FRONT_END_SERVER_PORT
from inventory import servers


class Document:
    def __init__(self, document_id, score):
        self.document_id = document_id
        self.score = score

class DocumentResult:
    def __init__(self, url, title, source, time, snippet):
        self.url = url
        self.title = title
        self.source = source
        self.time = time
        self.snippet = snippet

class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.render("HTML/main.html", front_end_port=str(FRONT_END_SERVER_PORT))


class SectionHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        section = self.get_argument('s')
        section = section.strip()

        section_servers = servers['section_server']
        document_servers = servers['document_server']

        doc_id_score_tuple_list = list()
        for i in range(len(section_servers)):
            query_url = section_servers[i] + "/section?s=" + section
            response = yield http_client.fetch(query_url)
            raw_data = json.loads(response.body.decode('utf-8'))
            doc_id_score_tuple_list.extend(raw_data["postings"])

        # for document in doc_id_score_tuple_list:
        #     print(document)

        document_list = []
        for element in doc_id_score_tuple_list:
            document_list.append(Document(element[0], element[1]))

        sorted_document_list = sorted(document_list, key=operator.attrgetter('score'), reverse=True)

        if len(sorted_document_list) > 10:
            sorted_document_list = sorted_document_list[0:10]

        document_results = list()
        for i in range(len(sorted_document_list)):
            doc_id = sorted_document_list[i].document_id

            # todo
            # hash_value = int(hashlib.md5(str(doc_id).encode()).hexdigest()[:8], 16)
            hash_value = doc_id % DOCUMENT_SERVER_NUM
            # hash_value = hash(str(doc_id))
            document_server_id = hash_value
            # document_server_id = 2

            request = document_servers[document_server_id] + "/doc?doc_id=" + str(doc_id)
            response = yield http_client.fetch(request)
            document_map = dict()
            extract_information_from_document_server(document_map, response.body.decode('utf-8'))
            document_result = DocumentResult(document_map['url'], document_map['title'], document_map['source'],
                                             document_map['time'], document_map['snippet'])
            document_results.append(document_result)


        # return_map = dict()
        # return_map["results"] = detail_document_list
        # return_map["num_results"] = len(sorted_document_list)
        # self.write(json.dumps(return_map))

        # for detail_document in detail_document_list:
        #     document_results.append(document_result)
        self.render("HTML/result.html", documents=document_results)
        # self.render("HTML/template.html", title="My title", documents=document_results)


def extract_information_from_document_server(document_map, string):
    json_map = json.loads(string)
    json_map = json_map['results'][0]
    # todo
    document_map['snippet'] = 'This is temp snippet'
    document_map['title'] = json_map['title']
    document_map['url'] = json_map['url']
    document_map['source'] = json_map['source']
    document_map['time'] = json_map['time']


def main(port):
    app = tornado.web.Application([
        tornado.web.url(r"/section", SectionHandler),
        tornado.web.url(r"/", MainHandler),
    ])
    app.listen(port)
    print("[front end server] is listening on " + str(port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(FRONT_END_SERVER_PORT)



