
from tornado import process

from inventory import FRONT_END_SERVER_PORT
from inventory import SECTION_SERVER_NUM
from inventory import DOCUMENT_SERVER_NUM

from front_end_server import front_end_server
from section_server import section_server
from document_server import document_server


def main():

    # launch indexer
    # indexer.main()


    # task_id = process.fork_processes(1 + SECTION_SERVER_NUM + DOCUMENT_SERVER_NUM)

    task_id = process.fork_processes(1 + SECTION_SERVER_NUM + DOCUMENT_SERVER_NUM)

    if task_id == 0:
        # launch front end server
        front_end_server.main(FRONT_END_SERVER_PORT)
    elif (task_id >= 1) & (task_id < SECTION_SERVER_NUM + 1):
        # launch the index servers
        port = FRONT_END_SERVER_PORT + task_id
        section_server.main(port, task_id - 1)
    elif (task_id >= SECTION_SERVER_NUM + 1) & (task_id < SECTION_SERVER_NUM + DOCUMENT_SERVER_NUM + 1):
        # launch the document servers
        port = FRONT_END_SERVER_PORT + task_id
        document_server.main(port, task_id - 1 - SECTION_SERVER_NUM)

if __name__ == "__main__":
    main()
