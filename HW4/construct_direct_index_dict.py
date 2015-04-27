#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import os
import pickle

def main():
    if len(sys.argv) == 3:
        filename_index = sys.argv[1]
        filename_dict = sys.argv[2]
    else:
        filename_index = 'direct_index'
        filename_dict = 'dictionary_direct_index'

    dictionary = {}

    with open(filename_index, 'w') as file_index:

        for line in sys.stdin:
            doc_id, length, b64string = line.rstrip().split('\t', 2)
            doc_id = int(doc_id)
            length = int(length)
            offset = file_index.tell()
            file_index.write(b64string + '\n')
            dictionary[doc_id] = {'number_of_words': length, 'offset': offset, 'length': len(b64string)}


    print('DIRECT INDEX CREATED. file =', filename_index, end=',')
    print(' size = %.5f Mb' % (os.path.getsize(filename_index)/(1.0*(2**20))))
    with open(filename_dict, 'wb') as file_dict:
        pickle.dump(dictionary, file_dict)
    print('dictionary DUMPED. file =', filename_dict)
    print('dictionary\'s size on disk =', end='')
    print(' %.5f Mb' % (os.path.getsize(filename_dict)/(1.0*(2**20))))
    print('dictionary\'s size in memory = ', end='')
    print('%.5f Mb' % (sys.getsizeof(dictionary)/(1.0*(2**20))))

if __name__ == '__main__':
    main()
