import matplotlib.pyplot as plt
import sys

# 使い方: python plot_tour.py random-tour-3000.dat
if len(sys.argv) < 2:
    print("Usage: python plot_tour.py <tour_data_file>")
    sys.exit(1)

target_file = sys.argv[1]

x_coords = []
y_coords = []
cost_info = ""

with open(target_file, "r") as f:
    for line in f:
        if line.startswith("#"):
            # コメント行からコストの情報を抜き出してタイトル用にする
            if "Cost:" in line:
                cost_info = line.strip()
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            x_coords.append(int(parts[0]))
            y_coords.append(int(parts[1]))

# グラフのプロット
plt.figure(figsize=(8, 8))

# 都市を点でプロット
plt.scatter(x_coords[:-1], y_coords[:-1], color="red", zorder=5, label="Cities")
# 巡回路を線でプロット
plt.plot(x_coords, y_coords, color="blue", linestyle="-", linewidth=1.5, label="Tour Path")

# 開始都市（最初の要素）を少し目立たせる
plt.scatter(x_coords[0], y_coords[0], color="green", s=100, zorder=6, label="Start/End")

plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title(f"TSP Tour Shape ({target_file})\n{cost_info}")
plt.grid(True)
plt.legend()

# 画像として保存（拡張子を .png に変える）
output_png = target_file.replace(".dat", ".png")
plt.savefig(output_png)
print(f"Saved tour plot to {output_png}")
plt.show()