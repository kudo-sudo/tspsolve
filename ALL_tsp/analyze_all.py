import glob
import re
import numpy as np

def parse_result(filename):
    final_cost = None
    total_time = None
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            m = re.match(r'# Final Best Cost: (\d+)', line)
            if m:
                final_cost = int(m.group(1))
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                total_time = float(parts[0])
                break
    return final_cost, total_time

methods = ['random', 'swap', '2opt', 'sa']
problems = ['eil51', 'eil76', 'eil101']

for tsp in problems:
    print(f"\n=== {tsp} ===")
    for method in methods:
        pattern = f'results_{tsp}/result_{method}_*.dat'
        files = sorted(glob.glob(pattern))
        costs = []
        times = []
        for f in files:
            cost, time = parse_result(f)
            if cost is not None:
                costs.append(cost)
            if time is not None:
                times.append(time)

        if costs:
            costs = np.array(costs)
            print(f"\n  [{method}]")
            print(f"  試行回数: {len(costs)}")
            print(f"  平均コスト: {np.mean(costs):.2f}")
            print(f"  コスト標準偏差: {np.std(costs):.2f}")
            print(f"  最小コスト: {np.min(costs)}")
            print(f"  最大コスト: {np.max(costs)}")
        else:
            print(f"\n  [{method}] データなし")