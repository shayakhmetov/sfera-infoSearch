#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import zlib
import base64
from lxml import etree
import lxml.html
from lxml.html.clean import Cleaner
import re


def main():
    split_regex = re.compile('[^\W\d_]+', re.U)
    for line in sys.stdin:
        doc_id, raw_data = line.rstrip().split()
        raw_data = unicode(zlib.decompress(base64.b64decode(raw_data)), encoding='utf-8')
        cleaner = Cleaner(style=True)
        cleaned_data = cleaner.clean_html(raw_data)
        document = lxml.html.document_fromstring(cleaned_data)
        text = ' '.join(etree.XPath("//text()")(document))
        words = re.findall(split_regex, text)
        for word in words:
            sys.stdout.write((word.strip().lower() + '\t' + doc_id + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()

