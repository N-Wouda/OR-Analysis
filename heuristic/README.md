# Heuristic

The heuristic is described in the `report.pdf` file. It can be ran on a problem
instance in the `/data` directory from the repository root as follows
```
python -m heuristic data/<instance>.csv
```
and outputs a solution file to the `solutions/` directory. This solution file
will be named `oracs_<problem instance>.csv`.

The heuristic parameters can be changed in `constants.py`.
