#!/bin/bash
cat ./povarenok/1_100/docs-000.txt | python mapper.py | sort -k1 | uniq > map_combine_result.txt