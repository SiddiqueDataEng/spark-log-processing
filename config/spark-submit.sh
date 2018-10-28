#!/bin/bash
# Spark Submit Script for Log Processing

spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --driver-memory 4g \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 10 \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.adaptive.coalescePartitions.enabled=true \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.minExecutors=5 \
  --conf spark.dynamicAllocation.maxExecutors=20 \
  --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.0.0 \
  --py-files src/log_processor.py \
  src/log_processor.py \
  --input-path /data/logs/apache/*.log \
  --output-path /data/processed \
  --log-type apache
