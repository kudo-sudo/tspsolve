import matplotlib.pyplot as plt
import glob
import re
import numpy as np

def parse_dat(filename):
    times = []
    costs = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                try:
                    times.append(float(parts[0]))
                    costs.append(int(parts[1]))
                except ValueError:
                    pass
    return times, costs

methods = {
    'random': ('result_random_*.dat', 'blue'),
    'swap':   ('result_swap_*.dat',   'orange'),
    '2-opt':  ('result_2opt_*.dat',   'green'),
    'sa':     ('result_sa_*.dat',     'red'),
}

plt.figure(figsize=(10, 6))

for method, (pattern, color) in methods.items():
    files = sorted(glob.glob(pattern))
    for f in files:
        times, costs = parse_dat(f)
        plt.plot(times, costs, color=color, alpha=0.2)
    
    # 代表として1回目だけラベルをつける
    plt.plot([], [], color=color, label=method)

plt.xscale('log')
plt.xlabel('CPU Time (s)')
plt.ylabel('Cost')
plt.title('Cost Transition by CPU Time (10 runs)')
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig('cost_multi.png', dpi=150)
plt.show()
print("Saved: cost_multi.png")