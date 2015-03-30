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
        filename_index = 'inverted_index dictionary'
        filename_dict = 'dictionary'

    dictionary = {}
    with open(filename_index, 'w') as file_index:
        for line in sys.stdin:
            term, b64string = line.rstrip().split('\t')
            offset = file_index.tell()
            dictionary[term] = (offset, len(b64string))
            file_index.write(b64string)

    print('DICTIONARY\'s size in memory= ', sys.getsizeof(dictionary)/(1.0*(2**20)), 'Mb')
    print('FINAL INDEX CREATED. file =', filename_index, ' size = ', os.path.getsize(filename_index)/(1.0*(2**20)), 'Mb')
    with open(filename_dict, 'w') as file_dict:
        pickle.dump(dictionary, file_dict)
    print('DICTIONARY DUMPED. file =', filename_dict)
    print('DICTIONARY\'s size on disk = ', os.path.getsize(filename_dict)/(1.0*(2**20)), 'Mb')



    # with open(filename_dict, 'r') as file_dict:
    #     dictionary = pickle.load(file_dict)
    #     for key in sorted(dictionary.keys()):
    #         print(key, dictionary[key])


if __name__ == '__main__':
    main()
