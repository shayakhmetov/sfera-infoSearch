#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import base64
import simple9
import varbyte
import os
import pickle
import math
sys.path.append(os.path.dirname(__file__))


def convert_to_differences(nums):
    current_num = 0
    for num in nums:
        if num < current_num:
            print('data\'s not sorted', file=sys.stderr)
            exit(1)
        yield num - current_num
        current_num = num


def write_result(term, term_doc_ids, number_all_docs, docs_lengths, encode_function=simple9.encode):
    unique_doc_ids = []
    for doc_id in sorted(term_doc_ids.keys()):
        unique_doc_ids.append((doc_id, sorted(term_doc_ids[doc_id])))
    doc_ids = [u[0] for u in unique_doc_ids]

    b64string = base64.b64encode(''.join([chr(x) for x in encode_function(convert_to_differences(doc_ids))]))
    sys.stdout.write((term + '\t' + b64string + '\t').encode('utf-8'))
    b64string = None

    tfs = [len(u[1]) for u in unique_doc_ids]
    idf = math.log(1.0*number_all_docs/len(tfs), 10)
    b = 0.75
    k1 = 2.0

    tfidfs = [int(round(tf*idf/(tf + k1*(b + docs_lengths[doc_ids[i]]*(1.0 - b))), 5)*(10**5)) for i, tf in enumerate(tfs)]
    tfidfs = base64.b64encode(''.join([chr(x) for x in encode_function(tfidfs)]))
    sys.stdout.write((tfidfs + '\t').encode('utf-8'))
    tfs, tfidfs = None, None
    b, k1, idf = None, None, None

    coords = [base64.b64encode(''.join([chr(x) for x in encode_function(convert_to_differences(u[1]))])) for u in unique_doc_ids]
    coords = ','.join(coords)
    unique_doc_ids = None

    sys.stdout.write((coords + '\n').encode('utf-8'))


def main():
    if len(sys.argv) == 3 and sys.argv[2] == 'vb':
        encode = varbyte.encode
    else:
        encode = simple9.encode
    if len(sys.argv) >= 2:
        filename_direct_dictionary = sys.argv[1]
    else:
        filename_direct_dictionary = 'dictionary_direct_index'
    current_term = None
    with open(filename_direct_dictionary, 'r') as direct_dictionary_file:
        direct_dictionary = pickle.load(direct_dictionary_file)

        docs_lengths = {}
        for doc_id, val in direct_dictionary.items():
            docs_lengths[doc_id] = val['number_of_words']
        number_all_docs = len(docs_lengths)
        direct_dictionary.clear()

        doc_ids = {}
        for line in sys.stdin:
            line = unicode(line, encoding='utf-8')
            term, doc_id, coord = line.rstrip().split('\t')
            doc_id = int(doc_id)
            coord = int(coord)
            if current_term != term:
                if doc_ids:
                    write_result(current_term, doc_ids[current_term], number_all_docs, docs_lengths, encode_function=encode)
                current_term = term
                doc_ids[term] = {}
                if doc_id in doc_ids[term]:
                    doc_ids[term][doc_id].append(coord)
                else:
                    doc_ids[term][doc_id] = [coord]
            else:
                if doc_id in doc_ids[term]:
                    doc_ids[term][doc_id].append(coord)
                else:
                    doc_ids[term][doc_id] = [coord]
        if doc_ids:
            write_result(current_term, doc_ids[current_term], number_all_docs, docs_lengths, encode_function=encode)


if __name__ == '__main__':
    main()

