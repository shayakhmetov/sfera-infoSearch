#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys

current_url = None
current_url_citied = set()
current_url_reversed = set()

for line in sys.stdin:
    line = line.rstrip().split('\t')
    if len(line) == 1:
        url = line[0]
    elif len(line) == 2:
        url, url_cited = line
    elif len(line) == 3:
        url, url_reversed = line[0], line[1]

    if url == current_url:
        if len(line) == 2:
            current_url_citied.add(url_cited)
        elif len(line) == 3:
            current_url_reversed.add(url_reversed)
    else:
        if current_url:
            print(current_url, 1, 1, sep='\t', end='\t')
            if len(current_url_citied) > 0:
                print(*current_url_citied, sep=',', end='\t')
            else:
                print('~', end='\t')
            if len(current_url_reversed) > 0:
                print(*current_url_reversed, sep=',')
            else:
                print('~')

        current_url = url
        if len(line) == 2:
            current_url_citied = set([url_cited])
        elif len(line) == 3:
            current_url_reversed = set([url_reversed])
        else:
            current_url_citied = set()
            current_url_reversed = set()


if current_url:
    print(current_url, 1, 1, sep='\t', end='\t')
    if len(current_url_citied) > 0:
        print(*current_url_citied, sep=',', end='\t')
    else:
        print('~', end='\t')
    if len(current_url_reversed) > 0:
        print(*current_url_reversed, sep=',')
    else:
        print('~')

