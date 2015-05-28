#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys

d = 0.85
current_n = None
adj_list = None
result_p = 0.

for line in sys.stdin:
    line = line.rstrip().split('\t')
    if current_n != line[0]:
        if current_n:
            if adj_list is not None:
                print(current_n, 1-d + d*result_p, adj_list, sep='\t')
            else:
                print(current_n, 1-d + d*result_p, sep='\t')
        current_n = line[0]
        result_p = 0.
        adj_list = None

    if line[1] == 'U':
        result_p += float(line[2])
    elif len(line) == 3:
        adj_list = line[2]

if current_n:
    if adj_list is not None:
        print(current_n, 1-d + d*result_p, adj_list, sep='\t')
    else:
        print(current_n, 1-d + d*result_p, sep='\t')