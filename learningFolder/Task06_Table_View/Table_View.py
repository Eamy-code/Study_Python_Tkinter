import tkinter as tk
from tkinter import filedialog, ttk
import csv

root = tk.Tk()
root.title("CSV 表示の練習")
root.geometry("500x300")

# Treeview（表）を作成
tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)

def load_csv():
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        print("ファイルが選択されませんでした")
        return

    print("読み込むファイル:", filepath)

    # 既存の表内容をクリア
    tree.delete(*tree.get_children())

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 1行目 → ヘッダー
    header = rows[0]
    tree["columns"] = header
    tree["show"] = "headings"

    # 各列にヘッダー名を設定
    for col in header:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # 2行目以降 → データ
    for row in rows[1:]:
        tree.insert("", "end", values=row)

# 読み込みボタン
button = tk.Button(root, text="CSVを読み込む", command=load_csv)
button.pack(pady=10)

root.mainloop()




# --- ポイント ---
# ttk.Treeview は Tkinter の表形式ウィジェット
# tree["columns"] にヘッダー名を設定することで列構造が決まる
# tree.heading() でヘッダー表示
# tree.insert() に values=行データ を渡すと1行追加される
# tree.delete(*tree.get_children()) で表の中身を一度クリアしている

