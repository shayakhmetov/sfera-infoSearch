#!/usr/bin/env python
from __future__ import print_function
__author__ = 'rim'

import sys


for line in sys.stdin:
    line = line.rstrip().split('\t')
    if len(line) == 5:
        n, a, h, adj_list, rev_adj_list = line

        print(n, adj_list, rev_adj_list, sep='\t')

        if adj_list == '~':
            adj_list = None
        else:
            adj_list = adj_list.split(',')
            for m in adj_list:
                print(m, 'A', h, sep='\t')

        if rev_adj_list == '~':
            rev_adj_list = None
        else:
            rev_adj_list = rev_adj_list.split(',')
            for m in rev_adj_list:
                print(m, 'H', a, sep='\t')

    else:
        assert False
