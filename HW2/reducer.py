#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import base64
import simple9
import varbyte


def convert_to_differences(nums):
    current_num = 0
    for num in nums:
        if num < current_num:
            print('data\'s not sorted', file=sys.stderr)
            exit(1)
        yield num - current_num
        current_num = num


def write_result(term, doc_ids, encode_function=simple9.encode):
    doc_ids = sorted(doc_ids)
    doc_ids = convert_to_differences(doc_ids)
    b64string = base64.b64encode(''.join([chr(x) for x in encode_function(doc_ids)]))
    sys.stdout.write((term + '\t' + b64string + '\n').encode('utf-8'))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'vb':
        encode = varbyte.encode
    else:
        encode = simple9.encode
    current_term = None
    doc_ids = []
    for line in sys.stdin:
        line = unicode(line, encoding='utf-8')
        term, doc_id = line.rstrip().split('\t')
        doc_id = int(doc_id)
        if current_term != term:
            if doc_ids:
                write_result(current_term, doc_ids, encode_function=encode)

            current_term = term
            doc_ids = [doc_id]
        else:
            doc_ids.append(doc_id)
    if doc_ids:
        write_result(current_term, doc_ids, encode_function=encode)


if __name__ == '__main__':
    main()

