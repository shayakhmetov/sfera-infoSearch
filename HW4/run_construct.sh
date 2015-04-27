#!/bin/bash
echo "Constructing final index from raw index..."
cat raw_inverted_index | python construct_index_dict.py inverted_index dictionary docs_info