import hashlib
import getpass
import os

IS_DEBUG = True

BASE_URL = "http://linserv1.cims.nyu.edu"
# BASE_URL = "http://localhost"

FRONT_EDN_SERVER_NUM = 1
SECTION_SERVER_NUM = 3
DOCUMENT_SERVER_NUM = 3

MAX_PORT = 49152
MIN_PORT = 10000

MODEL_DIR = os.getcwd() + "/model"
DOC_SRV_DIR = os.getcwd() + "/document_server"
SEC_SRV_DIR = os.getcwd() + "/section_server"


UPDATE_PASSWORD = 'ILOVENYU'

BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
    (MAX_PORT - MIN_PORT) + MIN_PORT

FRONT_END_SERVER_PORT = BASE_PORT

servers = dict()

servers['front_end'] = "%s:%d" % (BASE_URL, FRONT_END_SERVER_PORT)
servers['section_server'] = ["%s:%d" % (BASE_URL, port) for port in range(BASE_PORT + 1,
                                                                            BASE_PORT + 1 + SECTION_SERVER_NUM)]
servers['document_server'] = ["%s:%d" % (BASE_URL, port) for port in range(BASE_PORT + 1 + SECTION_SERVER_NUM,
                                                                             BASE_PORT + 1 + SECTION_SERVER_NUM + DOCUMENT_SERVER_NUM)]

CRAWLER_DOC_DIRS = dict()
CRAWLER_DOC_DIRS['NBC'] = "/Crawler/NBC/nbc_crawled_document"
CRAWLER_DOC_DIRS['NYT'] = "/Crawler/NYT/nyt_crawled_document"
CRAWLER_DOC_DIRS['FOX'] = "/Crawler/FOX/fox_crawled_document"

FOX_DOC_DIR = os.getcwd() + "/Crawler/FOX"
NYT_DOC_DIR = os.getcwd() + "/Crawler/NYT"
NBC_DOC_DIR = os.getcwd() + "/Crawler/NBC"

CRAWLER_DUMP_DIRS = dict()
CRAWLER_DUMP_DIRS['NBC'] = "/Crawler/NBC/nbc_crawled_document_dumped"
CRAWLER_DUMP_DIRS['NYT'] = "/Crawler/NYT/nyt_crawled_document_dumped"
CRAWLER_DUMP_DIRS['FOX'] = "/Crawler/FOX/fox_crawled_document_dumped"


