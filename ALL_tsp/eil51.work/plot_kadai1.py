import matplotlib.pyplot as plt
import re

def parse_dat(filename):
    steps = []
    times = []
    costs = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 3:
                try:
                    steps.append(int(parts[0]))
                    times.append(float(parts[1]))
                    costs.append(int(parts[2]))
                except ValueError:
                    pass
            elif len(parts) == 2:  # 最初の"0 cost"の行
                try:
                    steps.append(int(parts[0]))
                    times.append(0.0)
                    costs.append(int(parts[1]))
                except ValueError:
                    pass
    return steps, times, costs

steps, times, costs = parse_dat('result_random_step.dat')

plt.figure(figsize=(10, 6))
plt.plot(steps, costs)
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Random Search - Cost Transition (1000 iterations)')
plt.grid(True)
plt.tight_layout()
plt.savefig('random_step.png', dpi=150)
plt.show()
print("Saved: random_step.png")