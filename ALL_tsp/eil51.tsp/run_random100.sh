mkdir -p results_random
for i in $(seq 1 100); do
    ./tspsolve eil51.tsp random 1000 > results_random/result_random_$i.dat
done