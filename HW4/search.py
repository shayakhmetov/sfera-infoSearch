#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import time
import codecs
import sys
import pickle
import base64
import varbyte
import simple9
import re


def convert_differences_to(nums):
    current_num = 0
    for num in nums:
        yield num + current_num
        current_num += num


def read_nums(b64string, decode_function=simple9.decode):
    encoded_string = base64.b64decode(b64string)
    return convert_differences_to(decode_function([ord(x) for x in encoded_string]))


def main():
    if len(sys.argv) == 5 and sys.argv[4] == 'vb':
        decode = varbyte.decode
        print('VarByte DECODING')
    else:
        decode = simple9.decode
        print('Simple9 DECODING')
    if len(sys.argv) >= 4:
        filename_index = sys.argv[1]
        filename_dict = sys.argv[2]
        filename_urls = sys.argv[3]
    else:
        filename_dict = 'dictionary'
        filename_index = 'inverted_index'
        filename_urls = 'urls.txt'

    with open(filename_dict, 'rb') as file_dict, open(filename_index, 'r') as file_index, open(filename_urls, 'r') as file_urls:
        urls = []
        for url_line in file_urls:
            doc_id, url = url_line.rstrip().split()
            assert int(doc_id) == len(urls)
            urls.append(url)
        dictionary = pickle.load(file_dict)
        line = print('Введите поисковый запрос или CTRL+D для выхода')
        line = sys.stdin.readline()
        while line:
            line = [t.strip() for t in line.rstrip().lower().split('and')]
            try:
                # print('Запрос: ', line)
                posting_lists = []
                for term in line:
                    if not term:
                        raise StandardError()
                    deny = False    # NOT operator
                    if re.match('not\s.*', term):
                        term = term[4:].strip()
                        deny = True
                    if term in dictionary:
                        offset, length = dictionary[term]['offset'], dictionary[term]['length']
                        file_index.seek(offset)
                        b64string, tfidfs = file_index.read(length).split('\t')

                        doc_ids = set(read_nums(b64string, decode_function=decode))

                        posting_lists.append((deny, doc_ids))
                    else:
                        raise StandardError(str(term) + ' нигде не встречается')

                result_urls = {}
                for i, pl in enumerate(sorted(posting_lists, key=lambda p: p[0])):
                    doc_ids = pl[1]
                    if pl[0]:
                        if i == 0:
                            result_urls = {doc_id for doc_id in range(len(urls)) if doc_id not in doc_ids}
                        else:
                            result_urls = {doc_id for doc_id in result_urls if doc_id not in doc_ids}
                    else:
                        if i == 0:
                            result_urls = doc_ids
                        else:
                            result_urls = {doc_id for doc_id in result_urls if doc_id in doc_ids}
                    if len(result_urls) == 0:
                        raise StandardError('\tСовпадений не найдено')
                for doc_id in result_urls:
                    print(urls[doc_id])
                print('\tНайдено', len(result_urls), 'совпадений')

            except StandardError, e:
                print(e)

            line = print('Введите поисковый запрос или CTRL+D для выхода')
            line = sys.stdin.readline()


if __name__ == '__main__':
    main()
