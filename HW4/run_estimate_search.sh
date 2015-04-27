#!/bin/bash
echo "Estimating search quality..."
python estimate_search.py inverted_index dictionary_inverted_index urls.txt marks/povarenok1000.tsv stop_words.txt