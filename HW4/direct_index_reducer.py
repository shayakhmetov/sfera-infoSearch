#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import os
import zlib
import base64
sys.path.append(os.path.dirname(__file__))


def main():
    n = 0
    for line in sys.stdin:
        n += 1
        docid, words = line.rstrip().split('\t', 1)
        words = words.split('\t')
        sys.stdout.write(docid + '\t' + str(len(words)) + '\t' + base64.b64encode(zlib.compress(','.join(words))) + '\n')


if __name__ == '__main__':
    main()

