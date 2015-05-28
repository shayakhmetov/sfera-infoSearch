#!/bin/sh

echo 'NEW ITERATION #1'
INPUT='graph/part*'
OUTPUT='page_rank_step1'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -file mapper.py reducer.py \
    -mapper mapper.py \
    -reducer reducer.py \
    -input ${INPUT} \
    -output ${OUTPUT}

for ((i=2;i<=30;i++))
do
    echo 'NEW ITERATION #'${i}
    INPUT=${OUTPUT}
    OUTPUT='page_rank_step'${i}

    hadoop fs -rm -r ${OUTPUT}
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper.py reducer.py \
        -mapper mapper.py \
        -reducer reducer.py \
        -input ${INPUT} \
        -output ${OUTPUT}
    hadoop fs -rm -r ${INPUT}

hadoop fs -text ${OUTPUT}/part* | sort -k2,2nr | head > ${OUTPUT}_top.txt
done

