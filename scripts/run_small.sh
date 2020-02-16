#!/usr/bin/env bash

pipenv shell

instances="data/small_*.csv"

for instance in $instances
do
  python -m heuristic $instance
done
