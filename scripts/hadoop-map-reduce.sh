#!/usr/bin/env bash

USER_DIR="/users/hduser"
INPUT_DIR="$USER_DIR/input"
OUTPUT_DIR="$USER_DIR/output"

# Clean up previous runs.
hdfs dfs -rm -r "$OUTPUT_DIR/*"

rows=( 100 1000 10000 100000 1000000 2000000 3000000 4000000 5000000 )
for i in "${rows[@]}"; do
  SECONDS=0

  INPUT_NAME="test-$i"

  hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
   -mapper $HOME/scripts/mapper.py \
   -reducer $HOME/scripts/reducer.py \
   -input "$INPUT_DIR/$INPUT_NAME.csv" \
   -output "$OUTPUT_DIR/$INPUT_NAME" \
   
  elapsedseconds=$SECONDS
  echo "Elapsed: $elapsedseconds"

  hdfs dfs -tail "$OUTPUT_DIR/$INPUT_NAME/part-00000";
done
