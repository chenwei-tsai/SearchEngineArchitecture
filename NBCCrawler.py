from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado import gen
from bs4 import BeautifulSoup
import json
import os, sys
# DIR = os.getcwd()
# sys.path.append(DIR + "/../../")

from inventory import NBC_DOC_DIR
import pickle
import time

crawled_document_set_file = NBC_DOC_DIR + '/nbc_crawled_document_set.pickle'

@gen.coroutine
def get_page_links(url_set, url, layer):

    if url in url_set:
        return
    elif layer > 100:
        return

    http_client = httpclient.AsyncHTTPClient()
    request = httpclient.HTTPRequest(
        url=url,
        method="GET",
        validate_cert=False
    )

    try:
        future = http_client.fetch(request)
        response = yield future
    except Exception as e:
        print()
        print(e)
        print('failed to fetch ' + url)
        print()
        raise gen.Return()

    html = response.body if isinstance(response.body, str) \
        else response.body.decode()

    soup = BeautifulSoup(html, "html5lib")
    for link in soup.find_all('a'):

        try:
            url = link.get('href')
            if url is None:
                continue
            if url.startswith('http://') or url.startswith('https://'):
                continue
            elif url.startswith('/'):
                url = 'http://www.nbcnews.com' + url
                if url not in url_set:
                    url_set.add(url)
                    get_page_links(url_set, url, layer + 1)
        except Exception as e:
            print()
            print(e)
            print(type(url))
            print()


@gen.coroutine
def fetch_document(url, crawled_document_set):

    http_client = httpclient.AsyncHTTPClient()
    request = httpclient.HTTPRequest(
        url=url,
        method="GET",
        validate_cert=False
    )

    try:
        future = http_client.fetch(request)
        response = yield future
    except Exception as e:
        print()
        print(e)
        print('failed to fetch ' + url)
        print()
        raise gen.Return()

    html = response.body if isinstance(response.body, str) \
        else response.body.decode()

    soup = BeautifulSoup(html, "html5lib")

    article_body = soup.find("div", class_="article-body")
    time = soup.find('time', class_="timestamp_article")

    if article_body is None or time is None:
        return
    else:
        try:
            title = soup.title.text
            time = time.text
            text = ''
            for content in article_body.contents:
                if content.name == 'p':
                    sentence = content.text.strip()
                    if not sentence.startswith('Follow NBC'):
                        text = text + ' ' + sentence
            text = text.strip()

            document = dict()
            document['title'] = title
            document['time'] = time
            document['text'] = text
            document['url'] = url
            document['source'] = "NBC"
            file_name = url.split('/')[-1].split('.')[0]

            folder = NBC_DOC_DIR + '/nbc_crawled_document'
            with open(folder + '/' + file_name + '.txt', 'w') as outfile:
                json.dump(document, outfile)

            print(file_name + ' crawled')
            crawled_document_set.add(file_name)
            pickle.dump(crawled_document_set, open(crawled_document_set_file, "wb"))

        except Exception as e:
            print()
            print(e)
            print('failed to fetch ' + url)
            print()

@gen.coroutine
def main():

    if os.path.exists(crawled_document_set_file):
        try:
            crawled_document_set = pickle.load(open(crawled_document_set_file, 'rb'))
        except:
            crawled_document_set = set()
    else:
        crawled_document_set = set()

    base_url_list = list()
    base_url_list.append('http://www.nbcnews.com')
    base_url_list.append('http://www.nbcnews.com/news/us-news')
    base_url_list.append('http://www.nbcnews.com/news/world')
    base_url_list.append('http://www.nbcnewyork.com/')
    base_url_list.append('http://www.nbcnews.com/politics')
    base_url_list.append('http://www.nbcnews.com/investigations')
    base_url_list.append('http://www.nbcnews.com/health')
    base_url_list.append('http://www.nbcnews.com/tech')
    base_url_list.append('http://www.nbcnews.com/science')
    base_url_list.append('http://www.nbcsports.com/')

    while True:
        url_set = set()

        print('crawler started')
        for base_url in base_url_list:
            yield get_page_links(url_set, base_url, 1)
        print('crawler finished')

        print(len(url_set))
        for url in url_set:
            print(url)
            yield fetch_document(url, crawled_document_set)

        try:
            time.sleep(60 * 30)
        except Exception as e:
            print(e)
            print('crawler sleep interrupted')


if __name__ == '__main__':
    IOLoop.instance().run_sync(main)

