import matplotlib.pyplot as plt
import sys
import re

def parse_dat(filename):
    steps = []
    costs = []
    meta = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                # メタ情報をパース
                m = re.match(r'#\s+(\w+):\s+(.+)', line)
                if m:
                    meta[m.group(1)] = m.group(2)
            else:
                parts = line.split()
                if len(parts) == 2:
                    steps.append(int(parts[0]))
                    costs.append(int(parts[1]))
    return steps, costs, meta

# コマンドライン引数でファイルを複数受け取れる
# 例: python plot.py result_swap.dat result_2opt.dat
filenames = sys.argv[1:]
if not filenames:
    print("Usage: python plot.py <result.dat> [result2.dat ...]")
    sys.exit(1)

plt.figure(figsize=(10, 6))

for filename in filenames:
    steps, costs, meta = parse_dat(filename)
    label = meta.get('Neighborhood', filename)
    plt.plot(steps, costs, label=label)

plt.xlabel('Step')
plt.ylabel('Cost')
plt.title('Hill Climbing - Cost Transition')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('cost_transition.png', dpi=150)
plt.show()
print("Saved: cost_transition.png")