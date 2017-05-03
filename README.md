# Search Engine Architecture

This is a search engine architecture project maintained by Barry and Shawn

## Goal

The goal is to build a machine learning news topic classifier. We are going to write a few crawlers to crawl news articles from a few new source websites, and use the news articles crawled from The New York Times as our news topic training data. Hopefully in the end we could use the model we build to automatically classify all the news articles we crawled.


## How to launch the program:

Since we use some python2 sklearn packages, please run the codes in linux machine with python 2.7 and the corresponding sklearn packages

Please run below two lines of code in the root directory of SearchEngineArchitecture:

python start_web_server.py
python start_crawler_classifier.py

## How to test the program:

The program is deployed at

http://linserv2.cims.nyu.edu:27599

But somehow the NYU linserv2 something will kill a run program if the the section is out of time.
In this case please launch the program again

