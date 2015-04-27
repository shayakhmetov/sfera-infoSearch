#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import codecs
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
    else:
        decode = simple9.decode
    if len(sys.argv) >= 5:
        filename_index = sys.argv[1]
        filename_dict = sys.argv[2]
        filename_urls = sys.argv[3]
        filename_assessors = sys.argv[4]
        filename_stop_words = sys.argv[5]
    else:
        filename_dict = 'dictionary_inverted_index'
        filename_index = 'inverted_index'
        filename_urls = 'urls.txt'
        filename_assessors = 'marks/povarenok1000.tsv'
        filename_stop_words = 'stop_words.txt'

    with open(filename_dict, 'rb') as file_dict, open(filename_index, 'r') as file_index, \
        open(filename_urls, 'r') as file_urls, codecs.open(filename_assessors, 'r', encoding='utf-8') as file_assessors,\
        open(filename_stop_words, 'r') as file_stop_words:

        stop_words = []
        for line in file_stop_words:
            stop_words.append(line.strip())
        stop_words = set(stop_words)

        urls = []
        for url_line in file_urls:
            doc_id, url = url_line.rstrip().split()
            assert int(doc_id) == len(urls)
            urls.append(url)
        dictionary = pickle.load(file_dict)

        all_assessors = 0
        found_assessors = 0
        for line in file_assessors:
            all_assessors += 1
            words, good_url = line.strip().rsplit('\t', 1)
            words = [w.strip().lower() for w in words.split()]
            try:
                posting_lists = []
                tfidf_dictionary = {}
                words = [term for term in words if term not in stop_words]
                for term in words:
                    if not term:
                        raise StandardError()
                    if term in dictionary:
                        offset, length = dictionary[term]['offset'], dictionary[term]['length']
                        file_index.seek(offset)
                        b64string, tfidfs_b64, coords_b64 = file_index.read(length).split('\t', 2)

                        doc_ids = list(read_nums(b64string, decode_function=decode))

                        posting_lists.append(doc_ids)
                    else:
                        raise StandardError(str(term) + ' нигде не встречается')

                result_urls = {}
                for i, doc_ids in enumerate(sorted(posting_lists, key=lambda l: len(l))):
                    if i == 0:
                        result_urls = doc_ids
                    else:
                        result_urls = {doc_id for doc_id in result_urls if doc_id in doc_ids}
                    if len(result_urls) == 0:
                        raise StandardError('\tСовпадений не найдено')
                #result_urls = sorted(result_urls, key=lambda doc: sum([tfidf_dictionary[term].get(doc, 0.) for term in line]), reverse=True)
                for doc_id in result_urls:
                    if urls[doc_id] == good_url:
                        found_assessors += 1
                        break

                # print('\tНайдено', len(result_urls), 'совпадений')

            except StandardError, e:
                # print(e)
                pass
        print("%.2f" % (100.0*found_assessors/all_assessors), "% of assessments found", file=sys.stderr)

if __name__ == '__main__':
    main()
