from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado import gen
import json
from bs4 import BeautifulSoup
import time
import os
import pickle

base_url = 'https://api.nytimes.com/svc/news/v3/content/all/all.json'
api_key = 'a250db1c2ad749b290b633da7791a037'

@gen.coroutine
def main():
    crawled_document_set_file = 'nyt_crawled_document_set.pickle'
    if os.path.exists(crawled_document_set_file):
        try:
            crawled_document_set = pickle.load(open(crawled_document_set_file, 'rb'))
        except:
            crawled_document_set = set()
    else:
        crawled_document_set = set()

    while True:
        print('crawler started')
        url = base_url + '?api-key=' + api_key
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
            print('Failed to fetch newswire api')
            print()

        response_json = json.loads(response.body.decode('utf-8'))
        results = response_json['results']

        # for k, v in results[0].items():
        #     if isinstance(v, str):
        #         print(k + ': ' + v)
        #     else:
        #         print(k)
        #         print(v)

        for result in results:
            document_url = result['url']
            file_name = result['url'].split('/')[-1].split('.')[0]
            if file_name not in crawled_document_set:
                http_client2 = httpclient.AsyncHTTPClient()
                cookie = {
                    "Cookie": 'NYT-BCET=1494730372%7CUD9ePFkvdXpfhpUrb1QP%2FzMtX0g%3D%7CN%3B_%7CvWdnz6ipK3ulBmmHJ2qx0kpQBMkOJFukZoNLiLb4gls%3D; OX_plg=swf|shk|pm; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; RMID=007f0100561358f0398700b9; adxcs=-; __cfduid=d4ca3d0f80d07834d1104e2f76ad548791492138376; __gads=ID=aca3c4bc1ef75f63:T=1492138376:S=ALNI_Mbg_rNZlwT0qnHosoPiWKpTnWUQtA; _cb_ls=1; NYT_W2=New%20YorkNYUS|ChicagoILUS|London--UK|Los%20AngelesCAUS|San%20FranciscoCAUS|Tokyo--JP; nyt-d=101.000000000NAI00000s9Iny1/7GKH0720eC0U3GWJ055WO11Z8Yae0oFcLn1/FIm90LUXm70I5Xjy0NEJCm0g97y00U50eC1vA3Ch0rBdy00U0me21v7deS074X4Q0U3Hny1rQt9q1hUNHf1w70S20927no09U0u11wH5X1@ec0e7a36/dbaf8366; NYT-MPS=98aee58aff62eaedcb6d1a4df13924e1ee401148b801c762018b6ae7d8703641b90d0e941dd95d5b7d4fc510e21f43f6; anchorview1day=true; mnet_session_depth=3%7C1492138373128; OX_ssn=1093603980; OX_sd=3; optimizelyEndUserId=oeu1492138374040r0.9156152023450619; nyt-m=672CE8800B0209141F90529556219303&e=i.1493596800&t=i.10&v=i.6&l=l.15.2096568091.3444303452.2454916099.1035203483.1068496429.323244140.-1.-1.-1.-1.-1.-1.-1.-1.-1&n=i.2&g=i.0&rc=i.0&er=i.1492119623&vr=l.4.8.0.0.0&pr=l.4.26.0.0.0&vp=i.0&gf=l.10.2096568091.3444303452.2454916099.1035203483.1068496429.323244140.-1.-1.-1.-1&ft=i.0&fv=i.0&gl=l.2.-1.-1&rl=l.1.-1&cav=i.8&imu=i.1&igu=i.1&prt=i.5&kid=i.1&ica=i.1&iue=i.1&ier=i.0&iub=i.0&ifv=i.0&igd=i.0&iga=i.1&imv=i.0&igf=i.1&iru=i.0&ird=i.0&ira=i.1&iir=i.1; NYT-S=38WFlBwc2d0IzdR78UsAsLTQTTHcHQJmwmXjhEUY43dvhnQ/kCdhBbzJCRX.XPF39FSmqxFI1J4UBRVzsgGjLP43AoVB2fmoCc2K6ReKF/7q2yKW321p0tl0MYvLgIYarL.AH/t57fC1XinGujqcPpQejWWNbGhmPwJJ1.ZbB/ijHfBVU0M5h0RdLY4mp6j6OwBwVFmVNR1/3eCBQI4s1MIS/1aPmg1rUUvE6N8cUHkRZceM6/kYd2auhFD3vC/lNrl/B6iWk8lHU0; walley=GA1.2.1547294334.1492138376; _cb=CBsZprsXTMFLEdVT; _chartbeat2=.1492119627599.1492138977706.1.Cz59GPCF7LuGDLKERurzj2_Czwj7R; _cb_svref=https%3A%2F%2Fmyaccount.nytimes.com%2Fauth%2Flogin%3FURI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F2017%252F04%252F13%252Fbusiness%252Fgm-expands-self-driving-car-operations-to-silicon-valley.html%253F_r%253D5; nyt-a=dd8591fa17a13bb75dceec11ee2f0482fb7596c073470e3deb759a9d80f600e7; _sp_id.75b0=f03db2a4cd93359d.1492138378.1.1492139038.1492138378; _sp_ses.75b0=*'}
                new_request = httpclient.HTTPRequest(
                    url=document_url,
                    method="GET",
                    validate_cert=False,
                    follow_redirects=False,
                    max_redirects=200,
                    headers=cookie
                )
                try:
                    future = http_client2.fetch(new_request)
                    response2 = yield future
                    html = response2.body if isinstance(response2.body, str) \
                        else response2.body.decode()
                    # print(html)
                    soup = BeautifulSoup(html, "html5lib")
                    text = ""
                    for text_body in soup.find_all('p', {'class': 'story-body-text story-content'}):
                        text = text + ' ' + text_body.text
                    text = text.strip()
                    # print(text)
                    # story-body-text story-content
                    # context = ssl._create_unverified_context()
                    # response = urlopen(document_url, context=context)
                    # print(response2)
                    document = dict()
                    document['title'] = result['title']
                    document['abstract'] = result['abstract']
                    document['source'] = result['source']
                    document['url'] = result['url']
                    document['item_type'] = result['item_type']
                    document['material_type_facet'] = result['material_type_facet']
                    document['section'] = result['section']
                    document['created_date'] = result['created_date']
                    document['published_date'] = result['published_date']
                    document['updated_date'] = result['updated_date']
                    document['text'] = text

                    folder = 'nyt_crawled_document'
                    with open(folder + '/' + file_name + '.txt', 'w') as outfile:
                        json.dump(document, outfile)

                    print(file_name + ' crawled')
                    crawled_document_set.add(file_name)
                    pickle.dump(crawled_document_set, open(crawled_document_set_file, "wb"))

                except Exception as e:
                    print()
                    print(e)
                    print(document_url)
                    print()

        print('crawler ended')
        try:
            time.sleep(60 * 10)
        except:
            print('crawler sleep interrupted')

if __name__ == '__main__':
    IOLoop.instance().run_sync(main)

