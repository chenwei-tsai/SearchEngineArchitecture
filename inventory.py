import hashlib
import getpass

IS_DEBUG = True

DEBUG_ADDRESS = 'http://localhost'
DEPLOY_SERVER = 'http://newyorktimes.eastus.cloudapp.azure.com/'

FRONT_EDN_SERVER_NUM = 1
SECTION_SERVER_NUM = 3
DOCUMENT_SERVER_NUM = 3

MAX_PORT = 49152
MIN_PORT = 10000

BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
    (MAX_PORT - MIN_PORT) + MIN_PORT

FRONT_END_SERVER_PORT = BASE_PORT

servers = dict()
servers['front_end'] = "http://localhost:%d" % FRONT_END_SERVER_PORT
servers['section_server'] = ["http://localhost:%d" % port for port in range(BASE_PORT + 1,
                                                                            BASE_PORT + 1 + SECTION_SERVER_NUM)]
servers['document_server'] = ["http://localhost:%d" % port for port in range(BASE_PORT + 1 + SECTION_SERVER_NUM,
                                                                             BASE_PORT + 1 + SECTION_SERVER_NUM + DOCUMENT_SERVER_NUM)]


