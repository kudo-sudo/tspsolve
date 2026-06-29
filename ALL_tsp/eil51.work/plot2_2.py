import matplotlib.pyplot as plt

steps = []
costs = []

# ファイルを読み込む（#で始まる行は自動的に無視される処理を入れる）
with open("random-eil51.dat", "r") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            steps.append(int(parts[0]))
            costs.append(int(parts[1]))

plt.figure(figsize=(10, 6))
plt.plot(steps, costs, label="Random Search", color="blue")
plt.xlabel("Iterations (Trial Count)")
plt.ylabel("Best Cost (Evaluation Value)")
plt.title("TSP Random Search Progress")
plt.grid(True)
plt.legend()
plt.savefig("random-eil51.png")
plt.show()