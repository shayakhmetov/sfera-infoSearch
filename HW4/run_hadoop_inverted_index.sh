#!/bin/sh

INPUT='/data/sites/povarenok.ru/all/docs*.txt'
OUTPUT='raw_inverted_index'
SRC='src_inverted_index'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files ${SRC}/ \
    -mapper 'src_inverted_index/inverted_index_mapper.py src_inverted_index/stop_words.txt' \
    -reducer 'src_inverted_index/inverted_index_reducer.py src_inverted_index/dictionary_direct_index_all' \
    -numReduceTasks 10 \
    -input ${INPUT} \
    -output ${OUTPUT}
