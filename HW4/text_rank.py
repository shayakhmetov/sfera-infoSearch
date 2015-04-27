#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'rim'
import sys
import simple9
import varbyte
import base64


def convert_differences_to(nums):
    current_num = 0
    for num in nums:
        yield num + current_num
        current_num += num


def read_nums(b64string, decode_function=simple9.decode):
    encoded_string = base64.b64decode(b64string)
    return convert_differences_to(decode_function([ord(x) for x in encoded_string]))


def count_rank(passage, tfidfs):
    features = []
    tfidf = sum(tfidfs)
    features.append(tfidf)
    sorted_passage = sorted(passage)
    difference = 1.0/(sorted_passage[-1] - sorted_passage[0] + 1)
    features.append(difference)
    near_beginning = 1.0/(sorted_passage[0]+1)
    features.append(near_beginning)
    weights = [1]*len(features)
    return sum([a*b for a, b in zip(features, weights)])


def sort_by_passage(words, doc_ids, tfidf_dictionary, coords_dictionary, decode_function=simple9.decode):
    doc_ranks = {}
    for doc_id in doc_ids:
        max_rank = 0
        coords = []
        tfidfs = []
        for word in words:
            index = tfidf_dictionary[word][doc_id][0]
            tfidfs.append(tfidf_dictionary[word][doc_id][1])
            doc_coords_b64 = coords_dictionary[word].split(',')[index]
            doc_coords = list(read_nums(doc_coords_b64, decode_function=decode_function))
            coords.append(doc_coords)
        while all([len(c) > 0 for c in coords]):
            passage = [c[0] for c in coords]
            rank = count_rank(passage, tfidfs)
            if rank > max_rank:
                max_rank = rank
            min_index = 0
            for i, c in enumerate(coords):
                if c[0] < coords[min_index][0]:
                    min_index = i
            coords[min_index].pop(0)

        doc_ranks[doc_id] = max_rank

    return sorted(doc_ids, key=lambda d: doc_ranks[d], reverse=True)