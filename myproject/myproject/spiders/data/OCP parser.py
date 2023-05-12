# -*- coding: utf-8 -*-

from parsel import Selector
import os
import pandas as pd
name = "karger"


def parse(file):
    result = {
        'title': "",
        'journal': "",
        'pissn': "",
        'eissn': "",
        'pisbn': "",
        'eisbn': "",
        'doi': "",

        'volume': "",
        'issue': "",
        'year': "",
        'pages': "",

        'authors': [],
        'affiliations': [],
        'abstract': "",
        'references': [],
        'corresponding_authors': [],
        'keywords': [],
        'subjects': []
    }

    # TODO проблема в плохом форатировании HTML
    # TODO corresponding_authors
    # TODO affiliations

    with open(file, 'r', encoding="utf8", errors='ignore') as fp:
        data = fp.read()

    selector = Selector(text=data)

    s = selector.xpath('//div[@class="post-content"]/p/strong[string-length(text())>3]/text()')
    if (s):
        result['title'] = s[0].get()
    else:
        print(file + " title not found")

    s = selector.xpath('//title/text()')
    if (s):
        result['journal'] = s.get().split()[0]
    else:
        print(file + " journal not found")

    s = selector.xpath('//title/text()')
    if (s):
        result['volume'] = s.get().split()[1].split('.')[0]
    else:
        print(file + " volume not found")

    s = selector.xpath('//title/text()')
    try:
        result['issue'] = s.get().split()[1].split('.')[1].replace(',','')
    except:
        print(file + " issue not found")

    s = selector.xpath('//title/text()')
    if (s):
        result['pages'] = s.get().split()[3]
    else:
        print(file + " start page not found")

    s = selector.xpath('//div[@class="post-content"]/p/text()')
    if s:
        a=' '.join(s[0].get().split())
        b = a.split(' and')[0].split(',')
        b.append(a.split('and ')[-1])
        result['authors'].extend(b)

    s = selector.xpath('//div[@class="post-content"]/p/text()')
    if(len(s)>1):
        a = ' '.join(s[1].get().split())
        result['abstract'] = a


    s1=selector.xpath('//div[@class="post-content"]//em')
    if s1:
        if (len(s) > 2):
            a = ' '.join(s[2].get().split())
            result['keywords'].extend(a.split(','))
    return result


lt = os.listdir('full')
res = []
for i in lt:
    res.append(parse('full/'+i))
df = pd.DataFrame(res)
df.to_csv('OCP.csv', index=False, sep=';', encoding='UTF-8')

#print(lt)
#parse('full/'+'017b85f9d328ac3dbf0af35681eb0d4cdb69bdfb')