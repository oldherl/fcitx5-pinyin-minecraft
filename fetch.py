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
        "User-Agent": "PyFcitxDictBot/1.0; github.com/oldherl/fcitx5-pinyin-minecraft"
    }))

def fetch(url):
    res = open_request(url)
    if res.status == 200:
        return json.loads(res.read())
    else:
        raise StatusError(res.status)

def is_hanzi(c):
    # very rough. just to filter out basic latin.
    # U+3400 is the beginning of CJK ext A
    return c >= "\u3400"

def has_hanzi_parts(x):
    a = x.split('/')
    for s in a:
        if len(s) > 0 and is_hanzi(s[0]):
            return True
    return False

def get_variant(base_api_url, page_title, variant):
    data = fetch(base_api_url + "?action=query&prop=info&titles={}&inprop=varianttitles&format=json".format(quote_plus(page_title)))
    for i in data['query']['pages']:
        return (data['query']['pages'][i]['varianttitles'][variant])
    
def get_all_titles(base_api_url, output_filename, variant=None):
    articles = []
    data = fetch(base_api_url + "?action=query&list=allpages&format=json")
    count = 0
    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            count += 1
            if variant:
                if has_hanzi_parts(i):
                    t = get_variant(base_api_url, i, variant)
                    print(f"effective {len(articles)} out of {count}, last one {t}")
                    articles.append(t)
            else:
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

def get_all_categories(base_api_url, output_filename, variant=None):
    articles = []
    data = fetch(base_api_url + "?action=query&list=allcategories&format=json")
    count = 0
    while True:
        for i in map(lambda x: x["*"], data["query"]["allcategories"]):
            count += 1
            if variant:
                if has_hanzi_parts(i):
                    t = get_variant(base_api_url, i, variant)
                    print(f"effective {len(articles)} out of {count}, last one {t}")
                    articles.append(t)
            else:
                articles.append(i)
        print("Got {} pages".format(len(articles)))
        if "continue" in data:
            data = fetch(base_api_url + "?action=query&list=allcategories&format=json&aclimit=max&accontinue={}".format(
                quote_plus(data["continue"]["accontinue"])))
        else:
            break
    print("Finished.")
    with open(output_filename, "w") as f:
        f.write("\n".join(articles))

if __name__ == '__main__':
    operation = sys.argv[1]
    if operation == 'get_all_titles':
        base_api_url = sys.argv[2]
        output_filename = sys.argv[3]
        get_all_titles(base_api_url, output_filename)
    if operation == 'get_all_categories':
        base_api_url = sys.argv[2]
        output_filename = sys.argv[3]
        get_all_categories(base_api_url, output_filename)
    elif operation == 'get_variant':
        base_api_url = sys.argv[2]
        page_title = sys.argv[3]
        variant = sys.argv[4]
        get_variant(base_api_url, page_title, variant)
    elif operation == 'get_all_titles_in_variant':
        base_api_url = sys.argv[2]
        output_filename = sys.argv[3]
        variant = sys.argv[4]
        get_all_titles(base_api_url, output_filename, variant)
    else:
        print('No operation specified.')
    
