#!/bin/sh
INPUT='/data/sites/povarenok.ru/all/docs*.txt'
OUTPUT='graph'
hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file initial_mapper.py initial_reducer.py urls.txt \
        -mapper "initial_mapper.py" \
        -reducer "initial_reducer.py" \
        -input ${INPUT} \
        -output ${OUTPUT}

#hadoop fs -text ${OUTPUT}/part*
