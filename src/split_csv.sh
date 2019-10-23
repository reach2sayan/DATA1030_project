#!/bin/bash


HEADER=$(head -1 $1)
if [ -n "$2" ]; then
    CHUNK=$2
else 
    CHUNK=1000
fi
tail -n +2 $1 | split -l $CHUNK - $1_split_
for i in $1_split_*; do
    echo -e "$HEADER\n$(cat $i)" > $i
done

count=1
for f in ../data/data_raw.csv_split_*; do
    mv "$f" "../data/data_raw_$count.csv"
    count=$((count+1))
done

