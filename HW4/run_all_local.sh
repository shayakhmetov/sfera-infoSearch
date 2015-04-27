#!/bin/bash
./run_direct_index.sh
echo ""
./run_construct_direct_index.sh
echo ""
./run_inverted_index.sh
echo ""
./run_construct_inverted_index.sh
echo ""
./run_estimate_search.sh
