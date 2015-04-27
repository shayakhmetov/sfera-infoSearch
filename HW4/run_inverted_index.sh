#!/bin/bash
echo "Constructing raw INVERTED INDEX. Map phase..."
cat povarenok/1_100/docs-000.txt | python inverted_index_mapper.py stop_words.txt | sort -k1 > map_combine_result.txt
echo "Constructing raw INVERTED INDEX. Reduce phase..."
cat map_combine_result.txt | python inverted_index_reducer.py dictionary_direct_index > raw_inverted_index
