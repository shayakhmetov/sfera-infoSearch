#!/bin/bash
echo "Constructing final INVERTED INDEX from raw inverted index..."
cat raw_inverted_index_all | python construct_inverted_index_dict.py inverted_index_all dictionary_inverted_index_all