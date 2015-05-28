#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys


for line in sys.stdin:
    line = line.rstrip().split('\t')
    if len(line) == 2:
        n, page_rank = line
        print(n, page_rank, sep='\t')
    elif len(line) == 3:
        n, page_rank, adj_list = line
        print(n, page_rank, adj_list, sep='\t')

        adj_list = adj_list.split(',')
        adj_len = len(adj_list)
        for m in adj_list:
            print(m, 'U', float(page_rank)/adj_len, sep='\t')
    else:
        assert False
