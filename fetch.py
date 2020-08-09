#!/usr/bin/env python
import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, quote_plus
from retry import retry


class StatusError(Exception):
    def __init__(self, code):
        super().__init__("HTTP status is {}".format(code))


@retry()
def open_request(url):
    return urlopen(Request(url, headers={
        "User-Agent": "PyFcitxDictBot/1.0; github.com/outloudvi/fcitx5-pinyin-moegirl"
    }))

def fetch(url):
    res = open_request(url)
    if res.status == 200:
        return json.loads(res.read())
    else:
        raise StatusError(res.status)

def get_all_titles(base_api_url, output_filename):
    articles = []
    data = fetch(base_api_url + "?action=query&list=allpages&format=json")
    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            articles.append(i)
        print("Got {} pages".format(len(articles)))
        if "continue" in data:
            data = fetch(base_api_url + "?action=query&list=allpages&format=json&aplimit=max&apcontinue={}".format(
                quote_plus(data["continue"]["apcontinue"])))
        else:
            break
    print("Finished.")
    with open(output_filename, "w") as f:
        f.write("\n".join(articles))

def get_variant(base_api_url, page_title, variant):
    data = fetch(base_api_url + "?action=query&prop=info&titles={}&inprop=varianttitles&format=json".format(quote_plus(page_title)))
    for i in data['query']['pages']:
        return (data['query']['pages'][i]['varianttitles'][variant])


if __name__ == '__main__':
    operation = sys.argv[1]
    if operation == 'get_all_titles':
        base_api_url = sys.argv[2]
        output_filename = sys.argv[3]
        get_all_titles(base_api_url, output_filename)
    elif operation == 'get_variant':
        base_api_url = sys.argv[2]
        page_title = sys.argv[3]
        get_variant(base_api_url, page_title, 'zh-cn')
    else:
        print('No operation specified.')
    
