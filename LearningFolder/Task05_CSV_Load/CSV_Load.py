
import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.title("CSV読み込みの練習")
root.geometry("400x200")

def load_csv():
    # ファイル選択ダイアログの表示
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        print("ファイルが選択されませんでした")
        return

    print("読み込むファイル:", filepath)

    # CSVを読み込む処理
    with open(filepath, encoding="cp932") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)  # 行ごとに表示

button = tk.Button(root, text="CSVを読み込む", command=load_csv)
button.pack(pady=20)

root.mainloop()




# --- ポイント ---
# filedialog.askopenfilename() は OS 標準の「ファイルを開く」画面を出す
# filetypes=[("CSV Files", "*.csv")] により CSV のみに絞り込みが可能
# csv.reader() により CSV の内容を1行ずつ取得できる
# この Ticket では GUI への表示ではなく print で内容確認まで行う
