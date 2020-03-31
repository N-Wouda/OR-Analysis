# Validator

The validator is a simple tool meant to ensure a solution file is indeed 
feasible. The validator can be ran using
```
python -m validator data/<instance>.csv
```
and will validate the solution file associated with the problem instance (the
solution should be available in `solutions/`).

Note, of course, that the validator does not consider the quality of the 
solutions, only their feasibility.
