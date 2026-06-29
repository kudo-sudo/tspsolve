import re
import glob

methods = {
    'random': 'result_random_*.dat',
    'swap':   'result_swap_*.dat',
    '2-opt':  'result_2opt_*.dat',
    'sa':     'result_sa_*.dat',
}

for method, pattern in methods.items():
    costs = []
    files = sorted(glob.glob(pattern))
    for f in files:
        with open(f) as fp:
            for line in fp:
                m = re.match(r'# Final Best Cost: (\d+)', line)
                if m:
                    costs.append(int(m.group(1)))
    if costs:
        print(f"{method}: 平均={sum(costs)/len(costs):.1f} 最小={min(costs)} 最大={max(costs)} 回数={len(costs)}")
    else:
        print(f"{method}: データなし")