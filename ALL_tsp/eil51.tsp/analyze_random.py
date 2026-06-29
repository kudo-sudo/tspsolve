import glob
import re
import numpy as np

def get_final_cost(filename):
    with open(filename, 'r') as f:
        for line in f:
            m = re.match(r'# Final Best Cost: (\d+)', line)
            if m:
                return int(m.group(1))
    return None

files = sorted(glob.glob('results_random/result_random_*.dat'))

costs = []
for f in files:
    c = get_final_cost(f)
    if c is not None:
        costs.append(c)

costs = np.array(costs)

print(f"試行回数: {len(costs)}")
print(f"平均コスト: {np.mean(costs):.2f}")
print(f"分散: {np.var(costs):.2f}")
print(f"標準偏差: {np.std(costs):.2f}")
print(f"最小コスト: {np.min(costs)}")
print(f"最大コスト: {np.max(costs)}")