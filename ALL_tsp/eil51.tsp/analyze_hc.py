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
        # 最後のデータ行から時間を取得
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                total_time = float(parts[0])
                final_cost = int(parts[1])
                break
    return final_cost, total_time

for method, pattern in [('swap', 'results_hc_swap/result_*.dat'),
                         ('2-opt', 'results_hc_2opt/result_*.dat')]:
    files = sorted(glob.glob(pattern))
    costs = []
    times = []
    for f in files:
        cost, time = parse_result(f)
        if cost is not None and time is not None:
            costs.append(cost)
            times.append(time)

    costs = np.array(costs)
    times = np.array(times)

    print(f"\n=== {method} ===")
    print(f"試行回数: {len(costs)}")
    print(f"平均コスト: {np.mean(costs):.2f}")
    print(f"コスト分散: {np.var(costs):.2f}")
    print(f"コスト標準偏差: {np.std(costs):.2f}")
    print(f"最小コスト: {np.min(costs)}")
    print(f"最大コスト: {np.max(costs)}")
    print(f"平均計算時間: {np.mean(times):.4f} s")
    print(f"計算時間分散: {np.var(times):.6f}")
    print(f"計算時間標準偏差: {np.std(times):.4f} s")