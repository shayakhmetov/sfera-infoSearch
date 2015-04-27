#!/bin/bash
echo "Reduce phase..."
cat map_combine_result.txt | python reducer.py docs_info > raw_inverted_index