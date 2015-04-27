#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import zlib
import base64
from lxml import etree
import lxml.html
import codecs
from lxml.html.clean import Cleaner
import re


def main():
    split_regex = re.compile('[^\W\d_]+', re.U)
    if len(sys.argv) == 2:
        filename_stop_words = sys.argv[1]
    else:
        filename_stop_words = 'stop_words.txt'
    with codecs.open(filename_stop_words, 'r', encoding='utf-8') as file_stop_words:
        stop_words = []
        for line in file_stop_words:
            stop_words.append(line.strip())
        stop_words = set(stop_words)

        for line in sys.stdin:
            doc_id, raw_data = line.rstrip().split()
            raw_data = unicode(zlib.decompress(base64.b64decode(raw_data)), encoding='utf-8')
            cleaner = Cleaner(style=True)
            cleaned_data = cleaner.clean_html(raw_data)
            document = lxml.html.document_fromstring(cleaned_data)
            text = ' '.join(etree.XPath("//text()")(document))
            words = re.findall(split_regex, text)
            for word in words:
                lower_word = word.strip().lower()
                if lower_word not in stop_words:
                    sys.stdout.write((doc_id + '\t' + lower_word + '\t').encode('utf-8'))
            sys.stdout.write('\n')


if __name__ == '__main__':
    main()

