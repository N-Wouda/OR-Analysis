#!/usr/bin/env bash

pipenv shell

instances="data/small_*.csv"

for instance in $instances
do
  echo $instance
  python -m heuristic $instance
done
