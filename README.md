# VRPSPDMD-H (OR Analysis of Complex Systems)

[![Build Status](https://travis-ci.com/N-Wouda/OR-Analysis.svg?branch=master)](https://travis-ci.com/N-Wouda/OR-Analysis)

We study the vehicle routing problem with simultaneous pickup and delivery and
handling costs. A fleet of vehicles operates from a single depot to service all
customers, which need a a delivery or a pickup, but usually both. All delivery
items originate from the depot, and all pickup items go to the depot. The items
on the vehicles are organized as linear stacks where only the last loaded item
of each stack is accessible (LIFO). Handling operations are required if the 
delivery items are not the last loaded ones. 

We take exactly the situation as described in Hornstra et al. (2020). With one
exception: there are multiple linear stacks. The last item of each stack is 
directly accessible from the rear of the truck, regardless of the length of this
stack and regardless the length of the other stacks. The truck capacity is Q,
and there are σ stacks, hence maximum length of a stack is Q/σ. When loading 
items, it can be decided which stack(s) to put the item(s) in. Also when 
reconfiguring, a choice of stack must be made. 

A full report on our solution to this problem is made available in 
`heuristic/report.pdf`.

## How to use

For the heuristic, see `heuristic/README.md`. For the validator, see 
`validator/README.md`. Both assume the packages listed in the `Pipfile` are
available.

## References

* Hornstra, Richard P., Allyson Silva, Kees Jan Roodbergen, and Leandro C. 
  Coelho. 2020. "The vehicle routing problem with simultaneous pickup and
  delivery and handling costs". _Computers and Operations Research_. 115.
