#!/bin/bash
echo "Estimating search quality..."
cat marks/povarenok1000.tsv | python estimate_search.py inverted_index_all dictionary_inverted_index_all urls.txt stop_words.txt