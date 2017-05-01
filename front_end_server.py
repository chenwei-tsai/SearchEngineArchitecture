import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import operator
import hashlib

from inventory import FRONT_END_SERVER_PORT

class Document:
    def __init__(self, documentID, score):
        self.ducumentID = documentID
        self.score = score


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        # self.write('hello world')
        self.render("HTML/main.html", front_end_port=str(FRONT_END_SERVER_PORT))


class SectionHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        section = self.get_argument('section')

        items = ["Item 1", "Item 2", "Item 3"]
        self.render("HTML/template.html", title="My title", items=items)

        # index_server_base_address = "http://linserv2.cims.nyu.edu:"
        # index_server_base_port = 35315

        # list = []
        # for i in range(section_server_num):
        #     # query_url = index_server_base_address + str(index_server_base_port + i) + "/index?q=" + query
        #     query_url = INDEXER_SERVERS[i] + "/index?q=" + query.replace(" ", "%20")
        #     response = yield http_client.fetch(query_url)
        #     raw_data = json.loads(response.body.decode('utf-8'))
        #     list.extend(raw_data["postings"])
        #
        # documentList = []
        # for element in list:
        #     documentList.append(Document(element[0], element[1]))
        #
        # sortedDocumentList = sorted(documentList, key=operator.attrgetter('score'), reverse=True)
        #
        # if len(sortedDocumentList) > 10:
        #     sortedDocumentList = sortedDocumentList[0:10]
        #
        # detail_document_list = []
        # for i in range(len(sortedDocumentList)):
        #     id = sortedDocumentList[i].ducumentID
        #
        #     hash_value = int(hashlib.md5(str(id).encode()).hexdigest()[:8], 16)
        #     # hash_value = hash(str(id))
        #     document_server_id = hash_value % DocumentShardNumber
        #     # base = 35318
        #     # server = base + documentServerID
        #     # s = "http://linserv2.cims.nyu.edu:" + str(server) + "/doc?id=" + str(id) + "&q=" + query
        #     s = DOCUMENT_SERVERS[document_server_id] + "/doc?id=" + str(id) + "&q=" + query.replace(" ", "%20")
        #     response = yield http_client.fetch(s)
        #     document_map = {}
        #     extract_information_from_document_server(document_map, response.body.decode('utf-8'))
        #     detail_document_list.append(document_map)

        # return_map = {}
        # return_map["results"] = detail_document_list
        # return_map["num_results"] = len(sortedDocumentList)
        # self.write(json.dumps(return_map))


# def extract_information_from_document_server(document_map, string):
#     map = json.loads(string)
#     map = map["results"][0]
#     document_map["snippet"] = map["snippet"]
#     document_map["title"] = map["title"]
#     document_map["url"] = map["url"]

def main():

    port = FRONT_END_SERVER_PORT

    app = tornado.web.Application([
        tornado.web.url(r"/section", SectionHandler),
        tornado.web.url(r"/", MainHandler),
    ])
    app.listen(port)
    print("[front end server] is listening on " + str(port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()



