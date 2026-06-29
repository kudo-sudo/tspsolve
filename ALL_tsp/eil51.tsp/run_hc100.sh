mkdir -p results_hc_swap
mkdir -p results_hc_2opt
for i in $(seq 1 100); do
    ./tspsolve eil51.tsp hc swap  > results_hc_swap/result_$i.dat
    ./tspsolve eil51.tsp hc 2-opt > results_hc_2opt/result_$i.dat
done