#!/usr/bin/env bash

pipenv run

instances="data/small_*.csv"

for instance in $instances
do
  echo $instance
  python -m heuristic $instance
done
