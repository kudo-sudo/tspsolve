import matplotlib.pyplot as plt
import sys
import re

def parse_dat(filename):
    times = []
    costs = []
    meta = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                m = re.match(r'#\s+(\w+):\s+(.+)', line)
                if m:
                    meta[m.group(1)] = m.group(2)
            else:
                parts = line.split()
                if len(parts) == 2:
                    try:
                        times.append(float(parts[0]))
                        costs.append(int(parts[1]))
                    except ValueError:
                        pass
    return times, costs, meta

filenames = sys.argv[1:]
if not filenames:
    print("Usage: python plot_time.py <result.dat> [result2.dat ...]")
    sys.exit(1)

plt.figure(figsize=(10, 6))

for filename in filenames:
    times, costs, meta = parse_dat(filename)
    method = meta.get('Method', '')
    neighborhood = meta.get('Neighborhood', '')
    label = f"{method} {neighborhood}".strip()
    plt.plot(times, costs, label=label)

    plt.xscale('log')
    plt.xlabel('CPU Time (s)')
plt.ylabel('Cost')
plt.title('Cost Transition by CPU Time')
plt.legend()
plt.grid(True, which = 'both')
plt.tight_layout()
plt.savefig('cost_time.png', dpi=150)
plt.show()
print("Saved: cost_time.png")