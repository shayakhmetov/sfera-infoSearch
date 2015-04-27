#!/bin/bash
echo "Estimating search quality..."
cat marks/povarenok1000.tsv | python estimate_search.py inverted_index dictionary_inverted_index urls.txt stop_words.txt