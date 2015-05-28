#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys

d = 0.85

current_url = None
current_url_citied = set()
for line in sys.stdin:
    line = line.rstrip().split('\t')
    if len(line) == 1:
        url = line[0]
    elif len(line) == 2:
        url, url_cited = line

    if url == current_url:
        if len(line) == 2:
            current_url_citied.add(url_cited)
    else:
        if current_url and len(current_url_citied) > 0:
            print(current_url, 1-d, sep='\t', end='\t')
            print(*current_url_citied, sep=',')
        elif current_url:
            print(current_url, 1-d, sep='\t')

        current_url = url
        if len(line) == 2:
            current_url_citied = set([url_cited])
        else:
            current_url_citied = set()

if current_url and len(current_url_citied) > 0:
    print(current_url, 1-d, sep='\t', end='\t')
    print(*current_url_citied, sep=',')
elif current_url:
    print(current_url, 1-d, sep='\t')