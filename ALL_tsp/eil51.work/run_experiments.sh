#!/bin/bash
for i in $(seq 1 10); do
    ./tspsolve eil51.tsp random 3000  > result_random_$i.dat
    ./tspsolve eil51.tsp hc swap      > result_swap_$i.dat
    ./tspsolve eil51.tsp hc 2-opt     > result_2opt_$i.dat
    ./tspsolve eil51.tsp sa sa-params.cfg > result_sa_$i.dat
    echo "Run $i done"
done