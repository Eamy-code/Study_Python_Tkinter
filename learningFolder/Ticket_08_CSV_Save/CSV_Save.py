import tkinter as tk
from tkinter import filedialog, ttk
import csv

root = tk.Tk()
root.title("CSV 保存機能")
root.geometry("600x400")

# Treeview
tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)

# フィルタ UI
filter_frame = tk.Frame(root)
filter_frame.pack(fill="x", pady=10)

column_var = tk.StringVar()
column_box = ttk.Combobox(filter_frame, textvariable=column_var, state="readonly")
column_box.pack(side="left", padx=5)

cond_var = tk.StringVar()
cond_entry = tk.Entry(filter_frame, textvariable=cond_var)
cond_entry.pack(side="left", padx=5)

csv_data = []


def load_csv():
    """CSVの読み込み"""
    global csv_data

    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        print("ファイルが選択されませんでした")
        return

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        csv_data = list(reader)

    header = csv_data[0]
    rows = csv_data[1:]

    # Treeview セットアップ
    tree.delete(*tree.get_children())
    tree["columns"] = header
    tree["show"] = "headings"

    for col in header:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for row in rows:
        tree.insert("", "end", values=row)

    # Combobox に列名セット
    column_box["values"] = header
    column_box.current(0)


def apply_filter():
    """フィルタ実行"""
    if not csv_data:
        print("データが読み込まれていません")
        return

    header = csv_data[0]
    rows = csv_data[1:]

    target_col = column_var.get()
    condition = cond_var.get()

    if not target_col or not condition:
        print("条件を入力してください")
        return

    col_index = header.index(target_col)

    filtered = [row for row in rows if condition.lower() in row[col_index].lower()]

    tree.delete(*tree.get_children())
    for row in filtered:
        tree.insert("", "end", values=row)


def save_csv():
    """Treeview の内容を CSV に保存"""
    if not tree.get_children():
        print("保存するデータがありません")
        return

    # 保存先選択ダイアログ
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="保存先を選択してください"
    )
    if not filepath:
        return

    # Treeview のデータ抽出
    header = tree["columns"]
    rows = []

    for item in tree.get_children():
        rows.append(tree.item(item)["values"])

    # CSV 書き込み
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print("保存しました:", filepath)


# ボタン類
filter_button = tk.Button(filter_frame, text="フィルタ", command=apply_filter)
filter_button.pack(side="left", padx=5)

load_button = tk.Button(root, text="CSVを読み込む", command=load_csv)
load_button.pack(pady=5)

save_button = tk.Button(root, text="結果を保存", command=save_csv)
save_button.pack(pady=5)

root.mainloop()




# --- ポイント ---
# asksaveasfilename() により「保存ダイアログ」を表示
# tree.get_children() で表示中の行データの ID を取得できる
# tree.item(item)["values"] により 1 行分の値を取得できる
# writer.writerow(header) でヘッダーを書き出す
# writer.writerows(rows) で全行をまとめて書き出す
