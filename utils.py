import os
import time
from urllib.request import urlopen

RETRY = 2

def loadHTML(url):
    n = 0
    try:
        time.sleep(RETRY)
        print("[INFO]: " + url)
        cmd = "wget -O /tmp/A.txt " + url
        os.system(cmd)
        with open("/tmp/A.txt") as r:
            return r.read()
    except Exception as e:
        print(e)
        time.sleep(RETRY)
        n += 1
        if n >= RETRY:            
            return None
        return loadHTML(url) # Retry again...
