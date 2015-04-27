#!/bin/bash
echo "Constructing final DIRECT INDEX from raw direct index..."
cat raw_direct_index_all | python construct_direct_index_dict.py direct_index_all dictionary_direct_index_all