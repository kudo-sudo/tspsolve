#!/bin/bash

for tsp in eil51 eil76 eil101; do
    for i in $(seq 1 20); do
        ./tspsolve ${tsp}.tsp random 3000             > results_${tsp}/result_random_$i.dat
        ./tspsolve ${tsp}.tsp hc swap                 > results_${tsp}/result_swap_$i.dat
        ./tspsolve ${tsp}.tsp hc 2-opt                > results_${tsp}/result_2opt_$i.dat
        ./tspsolve ${tsp}.tsp sa sa-params-${tsp}.cfg > results_${tsp}/result_sa_$i.dat
        echo "${tsp} Run $i done"
    done
done