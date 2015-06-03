#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys

current_url = None
adj_list = None
rev_adj_list = None
result_a = 0
result_h = 0

for line in sys.stdin:
    line = line.rstrip().split('\t')
    if current_url != line[0]:
        if current_url:
            print(current_url, result_a, result_h, sep='\t', end='\t')
            if adj_list:
                print(adj_list, end='\t')
            else:
                print('~', end='\t')
            if rev_adj_list:
                print(rev_adj_list, sep=',')
            else:
                print('~')


        current_url = line[0]
        result_a = 0
        result_h = 0
        adj_list = None
        rev_adj_list = None

    if line[1] == 'A':
        result_a += int(line[2])
    elif line[1] == 'H':
        result_h += int(line[2])
    elif len(line) == 3:
        adj_list = line[1]
        rev_adj_list = line[2]


if current_url:
    print(current_url, result_a, result_h, sep='\t', end='\t')
    if adj_list:
        print(adj_list, end='\t')
    else:
        print('~', end='\t')
    if rev_adj_list:
        print(rev_adj_list, sep=',')
    else:
        print('~')