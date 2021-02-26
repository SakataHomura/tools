# -*- coding: utf-8 -*-
import sys
import time
import requests
import threading
from lxml import etree

rawurl = "https://yj1.7086xz.org/pw/thread.php?fid=22&page={0}"
host = "https://yj1.7086xz.org/pw/"

def detail_page(url, word, log):
    try:
        file = requests.get(url, timeout=5)
        data = file.content.decode('utf-8')
        #print(data)
        for wd in word:
            pos = data.find(wd)
            if pos != -1:
                with open(log, 'a') as f:
                    f.write(url)
                    f.write('\n')
                return 0
        return 0
    except Exception as r:
        print(r)
        return -1

def main_page(url, word, log):
    try:
        file = requests.get(url, timeout=5)
        data = file.content  
        html = etree.HTML(data)
        rows = html.xpath('//h3/a//@href')
        i = 0
        while i < len(rows):
            if not rows[i].startswith("html_data"):
                i = i + 1
                continue
            #print(rows[i])
            ret = detail_page(host+rows[i], word, log)
            if ret != 0:
                print(ret)
                continue
            i = i + 1  
        return 0
    except Exception as r:
        print(r)
        return -1

def run(start, end, word, log):
    for i in range(start, end):
        url = rawurl.format(i)
        print(url)
        ret = main_page(url, word, log)
        if ret != 0:
            print(ret)
            continue
        i = i + 1
        
if __name__ == "__main__":
    word = sys.argv[1].decode('gbk').split('|')
    total = int(sys.argv[2])
    log = sys.argv[3]
    print(word)
    
    ts = []
    if len(sys.argv) < 3:
        print("word, total, log")
    else:
        i = 1
        step = (total+10) / 10
        while i <= total:
            start = i
            end = start + step
            t = threading.Thread(target=run, args=(start, end, word, log,))
            ts.append(t)
            i = end
            
        for t in ts:
            t.start()
    
        for t in ts:
            t.join()
    
    
    #python bt.py 相沢 100 m.url