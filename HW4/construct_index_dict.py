#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import os
import pickle
import math
import base64


def main():
    if len(sys.argv) == 3:
        filename_index = sys.argv[1]
        filename_dict = sys.argv[2]
        filename_additional_info = sys.argv[3]
    else:
        filename_index = 'inverted_index'
        filename_dict = 'dictionary'
        filename_additional_info = 'additional_info'

    dictionary = {}

    with open(filename_index, 'w') as file_index, open(filename_additional_info, 'r') as file_additional_info:
        number_all_docs = int(file_additional_info.read().strip())
        for line in sys.stdin:
            term, b64string, tfs = line.rstrip().split('\t', 2)
            idf = math.log(1.0*number_all_docs/len(base64.b64decode(b64string)), 2)
            tfs = [int(tf) for tf in tfs.split(',')]
            tfidfs = [str(tf*idf) for tf in tfs]
            tfidfs = ','.join(tfidfs)
            offset = file_index.tell()
            file_index.write(b64string + '\t' + tfidfs + '\n')
            dictionary[term] = {'offset': offset, 'length': len(b64string) + len(tfidfs) + 1}


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
