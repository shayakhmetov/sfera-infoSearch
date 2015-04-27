#!/bin/sh

INPUT='/data/sites/povarenok.ru/all/docs*.txt'
OUTPUT='raw_inverted_index'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -files src/ \
    -mapper src/mapper.py \
    -reducer src/reducer.py \
    -numReduceTasks 5 \
    -input ${INPUT} \
    -output ${OUTPUT}
