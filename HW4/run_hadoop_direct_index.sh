#!/bin/sh

INPUT='/data/sites/povarenok.ru/all/docs*.txt'
OUTPUT='raw_direct_index'
SRC='src_direct_index'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files ${SRC}/ \
    -mapper 'src_direct_index/direct_index_mapper.py src_direct_index/stop_words.txt' \
    -reducer 'src_direct_index/direct_index_reducer.py'\
    -numReduceTasks 5 \
    -input ${INPUT} \
    -output ${OUTPUT}
