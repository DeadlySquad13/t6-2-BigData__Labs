#!/usr/bin/env bash

rows=( 100 1000 10000 100000 1000000 2000000 3000000 4000000 5000000 )
for i in "${rows[@]}"; do
  SECONDS=0
  
  INPUT_NAME="test-$i.csv"
  
  # Without sudo won't be able to read data files.
  if sudo python ./scripts/spark-map-reduce.py $INPUT_NAME; then
      elapsedseconds=$SECONDS
      echo "--- Elapsed $elapsedseconds s ---"
  else
      echo "There're errors executing python script, didn't count time"
  fi
done
