#
# Incrementally download and dump the chess games
#

import os
import sys
import urllib
import pickle
from lxml import html
from utils import loadHTML
from urllib.parse import urlsplit
from urllib.parse import parse_qsl

def readGameLinks(url, cur=1):
    links = []
    page = None
    out  = "step1/" + url.replace("/", "@") + ".html"
    if os.path.exists(out):
        with open(out) as r:
            data = r.read()
        assert(data is not None)
    else:
        print("Loading: " + url)
        data = loadHTML(url) # Read raw HTML
        assert(len(data) > 0)
        if data is None:
            return []
        with open(out, "w") as w:
            w.write(str(data))
    page = html.fromstring(data)
    hasNext = False
    nextURL = None
    for link in page.xpath("//a"):
        if link.get("href") != None:
            if 'page=' in link.get("href") and hasNext == False:
                page = link.get('href').split('page=')[1].split('&')[0]
                if not page.isdigit():
                    print("[WARN]: Not an integer. " + page + " " + url)
                    continue
                page = int(page)
                if page == cur + 1:
                    hasNext = True
                    nextURL = 'http://www.chessgames.com/' + link.get("href")
    if nextURL is not None:
        links = links + readGameLinks(nextURL, cur=cur+1)    
    return links

links = []
with open("players.tsv") as r:
    for line in r:
        toks = line.split("\t")
        assert(len(toks) == 2)
        links.append(toks[0])
assert(len(links) > 0)

urls = []
for link in links:
    for url in readGameLinks(link):
        urls.append(url)
with open("urls.pkl", "wb") as w:
    pickle.dump(urls, w)
