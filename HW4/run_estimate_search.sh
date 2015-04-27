#!/bin/bash
echo "Estimating search quality..."
cat marks/lenta1000.tsv | python estimate_search.py inverted_index dictionary_inverted_index povarenok/all/urls.txt stop_words.txt