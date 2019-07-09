import requests
from bs4 import BeautifulSoup
import bs4
import json
import re
import networkx as nx
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
        line_name = data['articleTitle']
        return html, line_name
    except:
        print("error")

def remove_last(text):
    if text == '南京站':
        return text
    if text == '南京南站':
        return text
    if text[-1] == '站':
        return text[:-1]
    return text

def fill_graph_by_oneline(graph, html, line_name):
    #use Beautifulsoup to extract data from table
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            # tds[0] from--to tds[1] distance
            if tds[0].string:
                match_obj = re.match(r'(.+)——(.+)', tds[0].string)
                if match_obj:
                    f = remove_last(match_obj.group(1))
                    t = remove_last(match_obj.group(2))
                    d = int(tds[1].string)
                    #print(f, t, d)
                    graph.add_edge(f, t, weight=d, line=line_name)

def save_graph(graph):
    f = open('nj_metro.defaultdict', 'wb')
    pickle.dump(graph, f)
    f.close()

if __name__ == '__main__':
    sub_links = get_data_sub_links()
    G = nx.Graph()
    for link in sub_links:
        html, line_name = download_data(link)
        fill_graph_by_oneline(G, html, line_name)
    save_graph(G)
