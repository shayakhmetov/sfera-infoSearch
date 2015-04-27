#!/bin/bash
echo "Generating raw DIRECT INDEX..."
cat lenta/1_100/docs-000.txt | python direct_index_mapper.py stop_words.txt | sort -nk1 | python direct_index_reducer.py > raw_direct_index
