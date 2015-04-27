#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import os
import pickle
import math
import base64
import simple9
import varbyte


def convert_differences_to(nums):
    current_num = 0
    for num in nums:
        yield num + current_num
        current_num += num

def read_nums(b64string, decode_function=simple9.decode):
    encoded_string = base64.b64decode(b64string)
    return convert_differences_to(decode_function([ord(x) for x in encoded_string]))


def main():
    decode = simple9.decode
    encode = simple9.encode
    if len(sys.argv) >= 3:
        filename_index = sys.argv[1]
        filename_dict = sys.argv[2]
        filename_additional_info = sys.argv[3]
        if len(sys.argv) == 5 and sys.argv[4] == 'vb':
            decode = varbyte.decode
            encode = varbyte.encode
    else:
        filename_index = 'inverted_index'
        filename_dict = 'dictionary'
        filename_additional_info = 'docs_info'

    dictionary = {}
    docs_lengths = {}
    with open(filename_index, 'w') as file_index, open(filename_additional_info, 'r') as file_additional_info:
        line_lengths = file_additional_info.readline().strip().split('\t')
        for doc_len in line_lengths:
            doc_id, length = [int(x) for x in doc_len.split(',')]
            docs_lengths[doc_id] = length
        number_all_docs = int(file_additional_info.readline().strip())
        for line in sys.stdin:
            term, b64string, tfs = line.rstrip().split('\t', 2)
            idf = math.log(1.0*number_all_docs/len(base64.b64decode(b64string)), 2)
            tfs = [int(tf) for tf in tfs.split(',')]
            b = 0.75
            k1 = 2.0
            doc_ids = list(read_nums(b64string, decode_function=decode))

            tfidfs = [int(round(tf*idf/(tf + k1*(b + docs_lengths[doc_ids[i]]*(1.0 - b))), 5)*(10**5)) for i, tf in enumerate(tfs)]
            tfidfs_b64 = base64.b64encode(''.join([chr(x) for x in encode(tfidfs)]))
            offset = file_index.tell()
            file_index.write(b64string + '\t' + tfidfs_b64 + '\n')
            dictionary[term] = {'offset': offset, 'length': len(b64string) + len(tfidfs_b64) + 1}


    print('DICTIONARY\'s size in memory = ', end='')
    print('%.5f Mb' % (sys.getsizeof(dictionary)/(1.0*(2**20))))
    print('FINAL INDEX CREATED. file =', filename_index, end='')
    print(' size = %.5f Mb' % (os.path.getsize(filename_index)/(1.0*(2**20))))
    with open(filename_dict, 'wb') as file_dict:
        pickle.dump(dictionary, file_dict)
    print('DICTIONARY DUMPED. file =', filename_dict)
    print('DICTIONARY\'s size on disk =', end='')
    print(' size = %.5f Mb' % (os.path.getsize(filename_dict)/(1.0*(2**20))))


if __name__ == '__main__':
    main()
