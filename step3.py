import os
import sys
import urllib
import pickle
import chess.pgn
from lxml import html

# Games in orders
gids = []

def readGameLinks(url, d):
    global gids
    links = []
    page = None
    assert(os.path.exists(url))
    toks = url.split("pid=")
    pid = int(toks[1].replace(".html", ""))

    with open(url) as r:
        page = html.fromstring(r.read())
        for link in page.xpath("//a"):
            if link.get("href") != None:
                if "gid" in link.get("href"):
                    gid = link.get("href").split("gid=")[1].split("&")[0]
                    gids.append(gid)

    if (d == 0):
        pid = int(url.replace(".html", "").split("pid=")[1])
        url = "step1/http:@@www.chessgames.com@@perl@chess.pl?page=2&pid=" + str(pid) + ".html"
        if os.path.exists(url):
            readGameLinks(url, 1)
    else:
        pid = int(url.split("page=")[1].split("&")[0])
        url = url.replace("page=" + str(pid), "page=" + str(pid + 1))
        if os.path.exists(url):
            readGameLinks(url, 1)

links = []
with open("players.tsv") as r:
    for line in r:
        toks = line.split("\t")
        assert(len(toks) == 2)
        readGameLinks("step1/" + toks[0].replace("/", "@") +  ".html", 0)

def fixName(x):
    x = x.replace("(Computer)", "")
    return x.strip()

assert(os.path.exists("step1"))
assert(os.path.exists("step2"))

w = {}

with open("players.tsv") as r:
    for line in r:
        toks = line.strip().split("\t")
        assert(len(toks) == 2)
        name = toks[1].replace('"', "")
        assert(len(name) > 0)
        w[name] = { "name":name,
                    "first":name.split(" ")[0],
                    "writer":open(name + ".pgn", "w") }
assert(len(w) > 0)

ignored = ["1002083", "1119705", "1130714", "1119705", "1130714", "1002269"]

for gid in gids:
    if gid in ignored:
        continue
    if not os.path.exists("step2" + os.sep + gid):
        print(gid)
    assert(os.path.exists("step2" + os.sep + gid))
    try:
        with open("step2" + os.sep + gid) as r:
            game  = chess.pgn.read_game(r)
            white = fixName(game.headers["White"])
            black = fixName(game.headers["Black"])
            assert(len(white) > 0)
            assert(len(black) > 0)
            
            if white == "?" or black == "?":
                continue
            elif white == "The World" or black == "The World":
                continue
            elif white == "Team White":
                continue

            if white not in w:
                toks = white.split(" ")
                for tok in toks:
                    for key in w:
                        if tok in key:
                            white = key

            if black not in w:
                toks = black.split(" ")
                for tok in toks:
                    for key in w:
                        if tok in key:
                            black = key

            n = 0
            if white in w:
                n += 1
                w[white]["writer"].write(str(game) + "\n\n")
            if black in w:
                n += 1
                w[black]["writer"].write(str(game) + "\n\n")
                
            if n == 0:
                print(n)
                print(gid)
                print(white)
                print(black)
                sddsaasdadsasdadssad
            
            if n == 0:
                print(gid)
            assert(n > 0)
    except Exception as e:
        print("Throw out: " + str(gid))

for i in w:
    w[i]["writer"].close()
