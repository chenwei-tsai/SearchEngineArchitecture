import sys,os
sys.path.append(os.getcwd() + "/../")
from inventory import CRAWLER_DOC_DIRS, CRAWLER_DUMP_DIRS

DIR = os.getcwd()

l = ["NYT", "NBC", "FOX"]

for i in l:
    doc_dir = DIR + "/../" + CRAWLER_DOC_DIRS[i]
    dump_dir = DIR + "/../" + CRAWLER_DUMP_DIRS[i]
    os.system("mv {}/* {}".format(dump_dir, doc_dir))
