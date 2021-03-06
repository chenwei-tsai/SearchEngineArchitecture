# Search Engine Architecture

This is a search engine architecture project maintained by Barry and Shawn

## Goal

The goal is to build a machine learning news topic classifier. We are going to write a few crawlers to crawl news articles from a few new source websites, and use the news articles crawled from The New York Times as our news topic training data. Hopefully in the end we could use the model we build to automatically classify all the news articles we crawled.


## How to launch the program:

Since we use some python2 sklearn packages, please run the codes in linux machine with python 2.7 and the corresponding sklearn packages

Please run below codes in the root directory of SearchEngineArchitecture:

* `python start_web_server.py`
* `python FOXCrawler.py`
* `python NBCCrawler.py`
* `python NYTCrawler.py`
* `python update_servers.py`

## How to test the program:

The program is deployed at

http://linserv1.cims.nyu.edu:27599/

But somehow the NYU linserv1 sometimes will kill a run program if the session is running out of time. In this case please launch the program again by typing above commands.

