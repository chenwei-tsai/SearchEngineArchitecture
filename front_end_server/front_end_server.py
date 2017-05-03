import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import operator
import datetime
import hashlib

from inventory import DOCUMENT_SERVER_NUM
from inventory import FRONT_END_SERVER_PORT
from inventory import servers, BASE_URL
from util import datetime_diff


class Document:
    def __init__(self, document_id, score, time):
        self.document_id = document_id
        self.score = score
        self.time = time
        self.datetime = datetime.datetime.strptime(time, '%Y%m%d%H%M')


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
        self.render("HTML/main.html", host=BASE_URL, front_end_port=str(FRONT_END_SERVER_PORT))


class SectionHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        section = self.get_argument('s')
        section = section.strip()

        section_servers = servers['section_server']
        document_servers = servers['document_server']

        doc_id_score_time_tuple_list = list()
        for i in range(len(section_servers)):
            query_url = section_servers[i] + "/section?s=" + section
            response = yield http_client.fetch(query_url)
            raw_data = json.loads(response.body.decode('utf-8'))
            doc_id_score_time_tuple_list.extend(raw_data["postings"])

        # < class 'list'>: [3042457829, [0.9959916585224816, '201704171344']]

        document_list = []
        for element in doc_id_score_time_tuple_list:
            document_list.append(Document(element[0], element[1][0], element[1][1]))

        sorted_document_list = sorted(document_list, key=operator.attrgetter('datetime'), reverse=True)


        if len(sorted_document_list) > 20:
            sorted_document_list = sorted_document_list[0:20]

        document_results = list()
        for i in range(len(sorted_document_list)):
            doc_id = sorted_document_list[i].document_id
            # print("doc id {}".format(doc_id))

            # hash_value = int(hashlib.md5(str(doc_id).encode()).hexdigest()[:8], 16)
            # hash_value = hash(str(doc_id))
            document_server_id = doc_id % DOCUMENT_SERVER_NUM

            request = document_servers[document_server_id] + "/doc?doc_id=" + str(doc_id)
            response = yield http_client.fetch(request)
            document_map = dict()
            extract_information_from_document_server(document_map, response.body.decode('utf-8'))
            print("document_map['time'] = {}".format(document_map['time']))
            document_datetime_object = datetime.datetime.strptime(document_map['time'], '%Y%m%d%H%M')
            time_diff = datetime_diff(document_datetime_object)

            document_result = DocumentResult(document_map['url'], document_map['title'], document_map['source'],
                                             time_diff, document_map['snippet'])
            document_results.append(document_result)


        # return_map = dict()
        # return_map["results"] = detail_document_list
        # return_map["num_results"] = len(sorted_document_list)
        # self.write(json.dumps(return_map))

        # for detail_document in detail_document_list:
        #     document_results.append(document_result)
        self.render("HTML/result.html", host=BASE_URL, front_end_port=FRONT_END_SERVER_PORT, documents=document_results),
        # self.render("HTML/template.html", title="My title", documents=document_results)


def extract_information_from_document_server(document_map, string):
    json_map = json.loads(string)
    # print(json_map)
    json_map = json_map['results'][0]
    # todo
    # document_map['snippet'] = 'This is temp snippet'
    document_map['snippet'] = json_map['snippet']
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



