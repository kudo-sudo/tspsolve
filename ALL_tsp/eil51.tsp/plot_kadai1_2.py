import matplotlib.pyplot as plt
import glob
import re
import os

def parse_tour(filename):
    x = []
    y = []
    cost = None
    rep = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('# Cost:'):
                cost = int(line.split(':')[1].strip())
            elif line.startswith('# Repetition:'):
                rep = line.split(':')[1].strip()
            elif not line.startswith('#'):
                parts = line.split()
                if len(parts) == 2:
                    x.append(int(parts[0]))
                    y.append(int(parts[1]))
    return x, y, cost, rep


files = sorted(glob.glob('random-tour-*.dat'), key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))

# 最大6つ表示
files_to_show = files[:5] + [files[-1]] if len(files) >= 6 else files

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, f in enumerate(files_to_show):
    x, y, cost, rep = parse_tour(f)
    axes[idx].plot(x, y, 'b-', linewidth=0.8)
    axes[idx].scatter(x[:-1], y[:-1], c='red', s=20, zorder=5)
    axes[idx].set_title(f'Iteration: {rep}\nCost: {cost}')
    axes[idx].grid(True)

plt.suptitle('Random Search - Tour Transitions', fontsize=14)
plt.tight_layout()
plt.savefig('random_tours.png', dpi=150)
plt.show()
print("Saved: random_tours.png")
