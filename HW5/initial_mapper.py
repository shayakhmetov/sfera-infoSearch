#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import zlib
import base64
from lxml import etree
import lxml.html
import re


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def main():
    regex = re.compile("https?://[www\.][^/]*\.povarenok\.ru.*")
    with open('urls.txt') as urls_file:
        urls_dict = {}
        for line in urls_file:
            id, url = line.rstrip().split()
            urls_dict[id] = url

        for line in sys.stdin:
            doc_id, raw_data = line.rstrip().split()
            raw_data = unicode(zlib.decompress(base64.b64decode(raw_data)), encoding='utf-8')
            document = lxml.html.document_fromstring(raw_data)
            urls = etree.XPath("//a/@href")(document)
            print(urls_dict[doc_id])
            for url in urls:
                if is_ascii(url):
                    if len(url) > 0 and url[0] == '/':
                        url = 'http://www.povarenok.ru' + url
                    if regex.match(url):
                        print(url)
                        print(urls_dict[doc_id], url, sep='\t')


if __name__ == '__main__':
    main()

