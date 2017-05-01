DOC_BASE_PORT = 27700
INDEX_BASE_PORT = 28800
conf = {
        "DOC_SERVERS": [DOC_BASE_PORT, DOC_BASE_PORT+1, DOC_BASE_PORT+2],
        "INDEX_SERVERS": [INDEX_BASE_PORT, INDEX_BASE_PORT+1, INDEX_BASE_PORT+2],
        "DOC_SRV_DIR": "/docserver/docdumps",
        "INDEX_SRV_DIR": "/indexserver/indexdumps",
        }
