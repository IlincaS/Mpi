# Mpi

The project provides a Python-based implementation and performance comparison of four SAT solving algorithms (resolution, DP, DPLL, CDCL).

This algorithms are evaluated on randomly generated 3-SAT instances to observe the differences in performance and behavior.

!!! The resolution solver is implemented but disabled due to its slow performance on large inputs. It can be enabled by uncommenting the lines from the bottom of the script. !!!

Example of an output:
Instance 1:
Clause 1: 1 ∨ -2 ∨ 3
...
Benchmarking DPLL...
DPLL times: [0.002, 0.001, 0.001]

Benchmarking DP...
DP times: [0.007, 0.002, 0.000]

Benchmarking CDCL...
CDCL times: [0.000, 0.000, 0.000]