#!/usr/bin/env bash

instances="data/small_*.csv"

for instance in $instances
do
  echo $instance
  pipenv run python -m heuristic $instance
done

pipenv run python -Om analysis "$instances" summary.csv
