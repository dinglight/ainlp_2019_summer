import requests
from bs4 import BeautifulSoup
import bs4
import json
import re
from collections import defaultdict
import pickle

def get_data_sub_links():
    base_link='http://www.njmetro.com.cn/njdtweb/portal/get-lineIntro.do?rowId='
    url = r'http://www.njmetro.com.cn/njdtweb/home/go-line-intro.do?columnId=8a8080076512510d0165130727520004&rowId=8a80800765a29a780165a8538b6f0018'
    response = requests.get(url)
    what_we_want = r'<a href="javascript:;" id="([0-9a-f]+)" onclick="changeLine\(id\)" class="ser_02_ta" style="width:40px;">(.+号线)</a>'
    pattern = re.compile(what_we_want)
    likes = pattern.findall(response.text)
    sub_links = []
    for like in likes:
        link, name = like
        sub_links.append(base_link + link)
    return sub_links

def download_data(url):
    """ download data """
    try:
        r = requests.get(url)
        #the text is a json, convert it to python dictionary
        data = json.loads(r.text)
        html = data['articleContent']
        return html
    except:
        print("error")

def fill_graph(graph, html):
    #use Beautifulsoup to extract data from table
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            # tds[0] from--to tds[1] distance
            if tds[0].string:
                match_obj = re.match(r'(.+)——(.+)', tds[0].string)
                if match_obj:
                    f = match_obj.group(1)
                    t = match_obj.group(2)
                    d = int(tds[1].string)
                    #print(f, t, d)
                    graph[f].append((t, d))
                    graph[t].append((f, d))

def save_graph(graph):
    f = open('nj_metro.defaultdict', 'wb')
    pickle.dump(graph, f)
    f.close()

if __name__ == '__main__':
    sub_links = get_data_sub_links()
    graph = defaultdict(list)
    for link in sub_links:
        html = download_data(link)
        fill_graph(graph, html)
    save_graph(graph)
