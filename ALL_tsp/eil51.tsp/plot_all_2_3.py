import matplotlib.pyplot as plt
import glob
import os

# 1. フォルダ内の「random-tour-数字.dat」というファイルをすべて集める
files = glob.glob("random-tour-*.dat")

if not files:
    print("エラー: random-tour-*.dat ファイルが見つかりません。先にC言語を実行してください。")
    exit(1)

# 2. 見つかったファイルを1つずつループ処理する
for target_file in files:
    x_coords = []
    y_coords = []
    cost_info = ""
    
    # ファイルの読み込み
    with open(target_file, "r") as f:
        for line in f:
            if line.startswith("#"):
                if "Cost:" in line:
                    cost_info = line.strip()
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                x_coords.append(int(parts[0]))
                y_coords.append(int(parts[1]))
                
    # データの読み込みに成功していればプロットを作成
    if x_coords and y_coords:
        plt.figure(figsize=(8, 8))
        
        # 都市（赤点）と巡回路（青線）を描画
        plt.scatter(x_coords[:-1], y_coords[:-1], color="red", zorder=5, label="Cities")
        plt.plot(x_coords, y_coords, color="blue", linestyle="-", linewidth=1.5, label="Tour Path")
        # スタート地点を目立たせる
        plt.scatter(x_coords[0], y_coords[0], color="green", s=100, zorder=6, label="Start/End")
        
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        
        # タイトルにファイル名とコストを記載
        plt.title(f"TSP Tour Shape ({target_file})\n{cost_info}")
        plt.grid(True)
        plt.legend()
        
        # 対応する拡張子を .png に変えて保存（画面表示はせず、保存だけ高速に行う）
        output_png = target_file.replace(".dat", ".png")
        plt.savefig(output_png)
        plt.close() # メモリ解放のためにグラフを閉じる
        

