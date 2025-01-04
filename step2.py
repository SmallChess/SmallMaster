import os
import sys
import urllib
import pickle
from lxml import html
from utils import loadHTML
from urllib.parse import urlsplit
from urllib.parse import parse_qsl

assert(os.path.exists("step1"))
games = []

cached = {}

# Everything already complete?
for file in os.listdir('step2'):
    cached[file] = True

for file in os.listdir('step1'):
    with open("step1" + os.sep + file) as r:
        page = html.fromstring(r.read())
        for link in page.xpath("//a"):
            if link.get("href") != None:
                if "gid" in link.get("href"):
                    gid = link.get("href").split("gid=")[1].split("&")[0]
                    if gid in cached:
                        continue
                    games.append({ "gid":gid, "link":"https://www.chessgames.com/perl/nph-chesspgn?text=1&gid=" + gid })

with open("step2.sh", "w") as w:
    for game in games:
        w.write("wget -O " + game["gid"] + " '" + game["link"] + "'\n")
        #w.write("sleep 10\n")
print("Generated: step2.sh")