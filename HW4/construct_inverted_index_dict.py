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
        filename_index = 'inverted_index'
        filename_dict = 'dictionary_inverted_index'

    dictionary = {}

    with open(filename_index, 'w') as file_index:

        for line in sys.stdin:
            term, b64string, tfidfs_b64, coords_b64 = line.rstrip().split('\t', 3)

            offset = file_index.tell()
            file_index.write(b64string + '\t' + tfidfs_b64 + '\t' + coords_b64 + '\n')
            dictionary[term] = {'offset': offset, 'length': len(b64string) + len(tfidfs_b64) + len(coords_b64) + 2}


    print('INVERTED INDEX CREATED. file =', filename_index, end=',')
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
